import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, User
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime

from config import EMOJI_PREMIUM, LANGUAGES, LANGUAGE_NAMES, ADMIN_IDS
from database import Database
from translator import Translator
from keyboards import (
    get_language_keyboard, get_main_keyboard, get_admin_keyboard, get_confirm_keyboard
)
from states import TranslateStates, AdminStates

logger = logging.getLogger(__name__)
router = Router()
db = Database()


# ==================== КОМАНДЫ ====================

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""
    user = message.from_user
    await db.add_user(user.id, user.username or "Unknown", user.first_name or "User")
    
    text = f"""
{EMOJI_PREMIUM['start']} **TranslateX - Премиум Переводчик**

{EMOJI_PREMIUM['diamond']} Добро пожаловать, {user.first_name}!

{EMOJI_PREMIUM['lightning']} Отправьте любой текст и выберите язык для перевода.

{EMOJI_PREMIUM['world']} Поддерживаемые языки:
🇷🇺 Русский | 🇺🇸 Английский | 🇵🇹 Португальский
🇩🇪 Немецкий | 🇫🇷 Французский | 🇪🇸 Испанский
🇮🇹 Итальянский | 🇹🇷 Турецкий | 🇺🇿 Узбекский

{EMOJI_PREMIUM['magic']} Используйте /help для справки
"""
    
    await message.answer(text, reply_markup=get_language_keyboard())
    await state.clear()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Команда /help"""
    text = f"""
{EMOJI_PREMIUM['info']} **СПРАВКА - Как использовать TranslateX**

{EMOJI_PREMIUM['lightning']} **Основные функции:**

1️⃣ Отправьте текст для перевода
2️⃣ Выберите целевой язык из предложенных
3️⃣ Получите красивый перевод {EMOJI_PREMIUM['magic']}

{EMOJI_PREMIUM['world']} **Доступные языки:**
🇷🇺 Русский | 🇺🇸 Английский | 🇵🇹 Португальский
🇩🇪 Немецкий | 🇫🇷 Французский | 🇪🇸 Испанский
🇮🇹 Итальянский | 🇹🇷 Турецкий | 🇺🇿 Узбекский

{EMOJI_PREMIUM['diamond']} **Команды:**
/start - Начать работу
/help - Эта справка
/admin - Админ панель (только для администраторов)

{EMOJI_PREMIUM['success']} Готовы? Отправьте текст!
"""
    await message.answer(text)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Команда /admin"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ запрещен!")
        return
    
    text = f"""
{EMOJI_PREMIUM['stats']} **АДМИН ПАНЕЛЬ**

Выберите действие:
"""
    await message.answer(text, reply_markup=get_admin_keyboard())


# ==================== ОБРАБОТКА ТЕКСТА ====================

@router.message(StateFilter(None), F.text)
async def handle_text(message: Message, state: FSMContext):
    """Обработка текста от пользователя"""
    user_id = message.from_user.id
    
    # Проверка бана
    if await db.is_banned(user_id):
        await message.answer(f"{EMOJI_PREMIUM['error']} Вы забанены!")
        return
    
    # Антиспам
    spam_count = await db.get_spam_count(user_id, minutes=1)
    if spam_count > 10:
        await db.log_spam(user_id, "spam_detected")
        await message.answer(f"{EMOJI_PREMIUM['error']} Слишком много запросов! Подождите...")
        return
    
    await db.log_spam(user_id, "translate_request")
    
    text = message.text.strip()
    
    if len(text) == 0 or len(text) > 5000:
        await message.answer(f"{EMOJI_PREMIUM['error']} Текст должен быть от 1 до 5000 символов!")
        return
    
    # Сохраняем текст в контексте
    await state.update_data(source_text=text)
    await state.set_state(TranslateStates.waiting_for_language)
    
    await message.answer(
        f"{EMOJI_PREMIUM['world']} Выберите язык для перевода:",
        reply_markup=get_language_keyboard()
    )


@router.callback_query(TranslateStates.waiting_for_language, F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора языка"""
    user_id = callback.from_user.id
    
    # Проверка бана
    if await db.is_banned(user_id):
        await callback.answer(f"{EMOJI_PREMIUM['error']} Вы забанены!", show_alert=True)
        return
    
    target_lang = callback.data.split("_")[1]
    data = await state.get_data()
    source_text = data.get("source_text", "")
    
    # Получаем язык пользователя
    user_lang = await db.get_language(user_id)
    
    # Переводим
    await callback.answer(f"{EMOJI_PREMIUM['lightning']} Переводим...", show_alert=False)
    
    translated = await Translator.translate(source_text, source_lang="auto", target_lang=target_lang)
    
    if translated:
        # Сохраняем в БД
        await db.add_translation(user_id, source_text, translated, "auto", target_lang)
        
        target_lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        
        result_text = f"""
{EMOJI_PREMIUM['success']} **Перевод выполнен!**

{EMOJI_PREMIUM['magic']} **Целевой язык:** {target_lang_name}

📝 **Результат:**
```
{translated}
```

{EMOJI_PREMIUM['diamond']} Отправьте еще текст для перевода!
"""
        await callback.message.answer(result_text)
    else:
        await callback.message.answer(
            f"{EMOJI_PREMIUM['error']} Ошибка при переводе. Попробуйте позже."
        )
    
    await state.clear()


# ==================== АДМИН ФУНКЦИИ ====================

@router.message(F.text.contains("Статистика"))
async def admin_stats(message: Message):
    """Статистика"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ запрещен!")
        return
    
    stats = await db.get_stats()
    
    text = f"""
{EMOJI_PREMIUM['stats']} **СТАТИСТИКА БОТА**

{EMOJI_PREMIUM['users']} Активных пользователей: {stats['total_users']}
{EMOJI_PREMIUM['translate']} Всего переводов: {stats['total_translations']}
{EMOJI_PREMIUM['ban']} Забанено пользователей: {stats['banned_users']}

{EMOJI_PREMIUM['diamond']} Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
    await message.answer(text)


@router.message(F.text.contains("Рассылка"))
async def admin_broadcast_start(message: Message, state: FSMContext):
    """Начало рассылки"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ запрещен!")
        return
    
    await state.set_state(AdminStates.waiting_for_broadcast)
    await message.answer(f"{EMOJI_PREMIUM['broadcast']} Отправьте текст для рассылки:")


@router.message(AdminStates.waiting_for_broadcast)
async def admin_broadcast_confirm(message: Message, state: FSMContext):
    """Подтверждение рассылки"""
    await state.update_data(broadcast_text=message.text)
    await state.set_state(AdminStates.confirm_broadcast)
    
    text = f"""
{EMOJI_PREMIUM['broadcast']} **Подтверждение рассылки**

Текст:
```
{message.text}
```

Вы уверены?
"""
    await message.answer(text, reply_markup=get_confirm_keyboard())


@router.callback_query(AdminStates.confirm_broadcast)
async def admin_broadcast_execute(callback: CallbackQuery, state: FSMContext):
    """Выполнение рассылки"""
    if callback.data == "confirm_no":
        await callback.message.answer(f"{EMOJI_PREMIUM['error']} Рассылка отменена")
        await state.clear()
        return
    
    data = await state.get_data()
    broadcast_text = data.get("broadcast_text", "")
    
    users = await db.get_all_users()
    sent = 0
    
    for user_tuple in users:
        try:
            user_id = user_tuple[0]
            await callback.bot.send_message(
                user_id,
                f"{EMOJI_PREMIUM['broadcast']} **Сообщение от администратора:**\n\n{broadcast_text}"
            )
            sent += 1
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
    
    await callback.message.answer(
        f"{EMOJI_PREMIUM['success']} Рассылка завершена!\n"
        f"Отправлено сообщений: {sent}"
    )
    await state.clear()


@router.message(F.text.contains("Бан"))
async def admin_ban_start(message: Message, state: FSMContext):
    """Начало процесса бана"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ запрещен!")
        return
    
    await state.set_state(AdminStates.waiting_for_ban_user_id)
    await message.answer(f"{EMOJI_PREMIUM['ban']} Отправьте ID пользователя для бана:")


@router.message(AdminStates.waiting_for_ban_user_id)
async def admin_ban_execute(message: Message, state: FSMContext):
    """Выполнение бана"""
    try:
        user_id = int(message.text)
        await db.ban_user(user_id)
        await message.answer(f"{EMOJI_PREMIUM['success']} Пользователь {user_id} забанен!")
    except ValueError:
        await message.answer(f"{EMOJI_PREMIUM['error']} Некорректный ID!")
    
    await state.clear()


@router.message(F.text.contains("Разбан"))
async def admin_unban_start(message: Message, state: FSMContext):
    """Начало процесса разбана"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ запрещен!")
        return
    
    await state.set_state(AdminStates.waiting_for_unban_user_id)
    await message.answer(f"{EMOJI_PREMIUM['unban']} Отправьте ID пользователя для разбана:")


@router.message(AdminStates.waiting_for_unban_user_id)
async def admin_unban_execute(message: Message, state: FSMContext):
    """Выполнение разбана"""
    try:
        user_id = int(message.text)
        await db.unban_user(user_id)
        await message.answer(f"{EMOJI_PREMIUM['success']} Пользователь {user_id} разбанен!")
    except ValueError:
        await message.answer(f"{EMOJI_PREMIUM['error']} Некорректный ID!")
    
    await state.clear()


@router.message(F.text.contains("Назад"))
async def admin_back(message: Message):
    """Вернуться в главное меню"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    await message.answer(
        f"{EMOJI_PREMIUM['start']} Главное меню",
        reply_markup=get_language_keyboard()
    )


# ==================== ОБРАБОТКА КНОПОК ====================

@router.message(F.text.contains("Выбрать язык"))
async def select_language(message: Message, state: FSMContext):
    """Выбор языка по умолчанию"""
    await message.answer(
        f"{EMOJI_PREMIUM['world']} Выберите язык по умолчанию:",
        reply_markup=get_language_keyboard()
    )


@router.callback_query(F.data.startswith("lang_"), StateFilter(None))
async def set_default_language(callback: CallbackQuery):
    """Установить язык по умолчанию"""
    target_lang = callback.data.split("_")[1]
    await db.set_language(callback.from_user.id, target_lang)
    
    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
    await callback.answer(
        f"{EMOJI_PREMIUM['success']} Язык установлен: {lang_name}",
        show_alert=True
    )


@router.message(F.text.contains("Перевести"))
async def start_translate(message: Message, state: FSMContext):
    """Начать перевод"""
    await state.set_state(TranslateStates.waiting_for_text)
    await message.answer(f"{EMOJI_PREMIUM['translate']} Отправьте текст для перевода:")
