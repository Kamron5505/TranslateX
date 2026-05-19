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

# Инициализируем db как None, будет установлена в main.py
db = None

def set_db(database):
    """Установить экземпляр БД"""
    global db
    db = database


# ==================== БУЙРУҚЛАР ====================

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""
    user = message.from_user
    await db.add_user(user.id, user.username or "Unknown", user.first_name or "User")
    
    text = f"""
Assalomu Aleykum ! 🧑‍💻

Siz aktiv xolatdasiz 📲

Quydagi menyudan tilni sozlab oling!
"""
    
    await message.answer(text, reply_markup=get_language_keyboard())
    await state.clear()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Команда /help"""
    text = f"""
{EMOJI_PREMIUM['info']} **ЁРДАМ - TranslateX ни қўллаш**

{EMOJI_PREMIUM['lightning']} **Асосий функциялар:**

1️⃣ Тарғима қилиш учун матнни юборинг
2️⃣ Таклиф қилинган тиллардан целевой тилни танланг
3️⃣ Чиройли тарғимани олинг {EMOJI_PREMIUM['magic']}

{EMOJI_PREMIUM['world']} **Мавжуд тиллар:**
🇷🇺 Русский | 🇺🇸 Английский | 🇵🇹 Португальский
🇩🇪 Немецкий | 🇫🇷 Французский | 🇪🇸 Испанский
🇮🇹 Итальянский | 🇹🇷 Турецкий | 🇺🇿 Ўзбек

{EMOJI_PREMIUM['diamond']} **Буйруқлар:**
/start - Ишни бошлаш
/help - Бу ёрдам
/admin - Админ панели (фақат администраторлар учун)

{EMOJI_PREMIUM['success']} Тайёрмисиз? Матнни юборинг!
"""
    await message.answer(text)


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Команда /admin"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ рад этилди!")
        return
    
    text = f"""
{EMOJI_PREMIUM['stats']} **АДМИН ПАНЕЛИ**

Амални танланг:
"""
    await message.answer(text, reply_markup=get_admin_keyboard())


# ==================== МАТННИ ИШЛАШ ====================

@router.message(StateFilter(None), F.text)
async def handle_text(message: Message, state: FSMContext):
    """Обработка текста от пользователя"""
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Проверка если это выбор языка
    if "Tilni tanlang" in text:
        # Извлекаем код языка из текста (например "ru" из "🇷🇺 Tilni tanlang (ru)")
        lang_code = text.split("(")[-1].rstrip(")")
        await db.set_language(user_id, lang_code)
        
        lang_name = LANGUAGE_NAMES.get(lang_code, lang_code)
        await message.answer(
            f"{EMOJI_PREMIUM['success']} Тил ўрнатилди: {lang_name}",
            reply_markup=get_language_keyboard()
        )
        return
    
    # Проверка бана
    if await db.is_banned(user_id):
        await message.answer(f"{EMOJI_PREMIUM['error']} Сиз блокланган!")
        return
    
    # Антиспам
    spam_count = await db.get_spam_count(user_id, minutes=1)
    if spam_count > 10:
        await db.log_spam(user_id, "spam_detected")
        await message.answer(f"{EMOJI_PREMIUM['error']} Жуда кўп сўровлар! Кутинг...")
        return
    
    await db.log_spam(user_id, "translate_request")
    
    if len(text) == 0 or len(text) > 5000:
        await message.answer(f"{EMOJI_PREMIUM['error']} Матн 1 дан 5000 белгигача бўлиши керак!")
        return
    
    # Сохраняем текст в контексте
    await state.update_data(source_text=text)
    await state.set_state(TranslateStates.waiting_for_language)
    
    await message.answer(
        f"{EMOJI_PREMIUM['world']} Тарғима қилиш учун тилни танланг:",
        reply_markup=get_language_keyboard()
    )


@router.message(TranslateStates.waiting_for_language, F.text)
async def handle_language_selection(message: Message, state: FSMContext):
    """Обработка выбора языка из Reply Keyboard"""
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Проверка бана
    if await db.is_banned(user_id):
        await message.answer(f"{EMOJI_PREMIUM['error']} Сиз блокланган!")
        await state.clear()
        return
    
    # Извлекаем код языка из текста (например "ru" из "🇷🇺 Tilni tanlang (ru)")
    if "Tilni tanlang" not in text:
        await message.answer(f"{EMOJI_PREMIUM['error']} Iltimos, тилни танланг!")
        return
    
    target_lang = text.split("(")[-1].rstrip(")")
    data = await state.get_data()
    source_text = data.get("source_text", "")
    
    # Переводим
    await message.answer(f"{EMOJI_PREMIUM['lightning']} Тарғима қилинмоқда...")
    
    translated = await Translator.translate(source_text, source_lang="auto", target_lang=target_lang)
    
    if translated:
        # Сохраняем в БД
        await db.add_translation(user_id, source_text, translated, "auto", target_lang)
        
        target_lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        
        result_text = f"""
{EMOJI_PREMIUM['success']} **Тарғима тайёр!**

{EMOJI_PREMIUM['magic']} **Целевой тил:** {target_lang_name}

📝 **Натижа:**
```
{translated}
```

{EMOJI_PREMIUM['diamond']} Яна матнни юборинг!
"""
        await message.answer(result_text, reply_markup=get_language_keyboard())
    else:
        await message.answer(
            f"{EMOJI_PREMIUM['error']} Тарғимада хато. Кейинроқ қўллаб кўринг.",
            reply_markup=get_language_keyboard()
        )
    
    await state.clear()


# ==================== АДМИН ФУНКЦИЯЛАРИ ====================

@router.message(F.text.contains("Статистика"))
async def admin_stats(message: Message):
    """Статистика"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ рад этилди!")
        return
    
    stats = await db.get_stats()
    
    text = f"""
{EMOJI_PREMIUM['stats']} **БОТ СТАТИСТИКАСИ**

{EMOJI_PREMIUM['users']} Фаол фойдаланувчилар: {stats['total_users']}
{EMOJI_PREMIUM['translate']} Жами тарғималар: {stats['total_translations']}
{EMOJI_PREMIUM['ban']} Блокланган фойдаланувчилар: {stats['banned_users']}

{EMOJI_PREMIUM['diamond']} Сана: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
    await message.answer(text)


@router.message(F.text.contains("Рассылка"))
async def admin_broadcast_start(message: Message, state: FSMContext):
    """Начало рассылки"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ рад этилди!")
        return
    
    await state.set_state(AdminStates.waiting_for_broadcast)
    await message.answer(f"{EMOJI_PREMIUM['broadcast']} Трансляция учун матнни юборинг:")


@router.message(AdminStates.waiting_for_broadcast)
async def admin_broadcast_confirm(message: Message, state: FSMContext):
    """Подтверждение рассылки"""
    await state.update_data(broadcast_text=message.text)
    await state.set_state(AdminStates.confirm_broadcast)
    
    text = f"""
{EMOJI_PREMIUM['broadcast']} **Трансляцияни тасдиқлаш**

Матн:
```
{message.text}
```

Сиз ишончи жойми?
"""
    await message.answer(text, reply_markup=get_confirm_keyboard())


@router.callback_query(AdminStates.confirm_broadcast)
async def admin_broadcast_execute(callback: CallbackQuery, state: FSMContext):
    """Выполнение рассылки"""
    if callback.data == "confirm_no":
        await callback.message.answer(f"{EMOJI_PREMIUM['error']} Трансляция бекор қилинди")
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
                f"{EMOJI_PREMIUM['broadcast']} **Администратордан сообщение:**\n\n{broadcast_text}"
            )
            sent += 1
        except Exception as e:
            logger.error(f"Фойдаланувчи {user_id} га сообщение юборишда хато: {e}")
    
    await callback.message.answer(
        f"{EMOJI_PREMIUM['success']} Трансляция тамомланди!\n"
        f"Юборилган сообщениялар: {sent}"
    )
    await state.clear()


@router.message(F.text.contains("Бан"))
async def admin_ban_start(message: Message, state: FSMContext):
    """Начало процесса бана"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ рад этилди!")
        return
    
    await state.set_state(AdminStates.waiting_for_ban_user_id)
    await message.answer(f"{EMOJI_PREMIUM['ban']} Блокланиши керак бўлган фойдаланувчи ID сини юборинг:")


@router.message(AdminStates.waiting_for_ban_user_id)
async def admin_ban_execute(message: Message, state: FSMContext):
    """Выполнение бана"""
    try:
        user_id = int(message.text)
        await db.ban_user(user_id)
        await message.answer(f"{EMOJI_PREMIUM['success']} Фойдаланувчи {user_id} блокланди!")
    except ValueError:
        await message.answer(f"{EMOJI_PREMIUM['error']} Нотўғри ID!")
    
    await state.clear()


@router.message(F.text.contains("Разбан"))
async def admin_unban_start(message: Message, state: FSMContext):
    """Начало процесса разбана"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer(f"{EMOJI_PREMIUM['error']} Доступ рад этилди!")
        return
    
    await state.set_state(AdminStates.waiting_for_unban_user_id)
    await message.answer(f"{EMOJI_PREMIUM['unban']} Блокни очиш керак бўлган фойдаланувчи ID сини юборинг:")


@router.message(AdminStates.waiting_for_unban_user_id)
async def admin_unban_execute(message: Message, state: FSMContext):
    """Выполнение разбана"""
    try:
        user_id = int(message.text)
        await db.unban_user(user_id)
        await message.answer(f"{EMOJI_PREMIUM['success']} Фойдаланувчи {user_id} блокни очилди!")
    except ValueError:
        await message.answer(f"{EMOJI_PREMIUM['error']} Нотўғри ID!")
    
    await state.clear()


@router.message(F.text.contains("Назад"))
async def admin_back(message: Message):
    """Вернуться в главное меню"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    await message.answer(
        f"{EMOJI_PREMIUM['start']} Асосий меню",
        reply_markup=get_language_keyboard()
    )


# ==================== ТУГМАЛАРНИ ИШЛАШ ====================

@router.message(F.text.contains("Выбрать язык"))
async def select_language(message: Message, state: FSMContext):
    """Выбор языка по умолчанию"""
    await message.answer(
        f"{EMOJI_PREMIUM['world']} Стандарт тилни танланг:",
        reply_markup=get_language_keyboard()
    )


@router.message(F.text.contains("Tilni tanlang"), StateFilter(None))
async def set_default_language(message: Message):
    """Установить язык по умолчанию"""
    text = message.text.strip()
    
    if "Tilni tanlang" not in text:
        return
    
    target_lang = text.split("(")[-1].rstrip(")")
    await db.set_language(message.from_user.id, target_lang)
    
    lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
    await message.answer(
        f"{EMOJI_PREMIUM['success']} Тил ўрнатилди: {lang_name}",
        reply_markup=get_language_keyboard()
    )


@router.message(F.text.contains("Перевести"))
async def start_translate(message: Message, state: FSMContext):
    """Начать перевод"""
    await state.set_state(TranslateStates.waiting_for_text)
    await message.answer(f"{EMOJI_PREMIUM['translate']} Тарғима қилиш учун матнни юборинг:")
