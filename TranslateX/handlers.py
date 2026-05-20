import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from config import EMOJI_PREMIUM, LANGUAGES, LANGUAGE_NAMES, ADMIN_IDS
from database import Database
from translator import Translator
from keyboards import (
    get_main_menu_keyboard, get_language_selection_keyboard, lang_name_to_code
)
from states import TranslateStates, AdminStates

logger = logging.getLogger(__name__)
router = Router()

db = None

def set_db(database):
    global db
    db = database


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = message.from_user
    await db.add_user(user.id, user.username or "Unknown", user.first_name or "User")
    
    text = f"Siz aktiv xolatdasiz\n\nQuydagi menyudan tilni sozlab oling!"
    
    await state.set_state(TranslateStates.main_menu)
    await message.answer(text, reply_markup=get_main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = f"""ℹ️ YORDAM - TranslateX

⚡ Asosiy funktsiyalar:

1️⃣ Tarjima qilish uchun matnni yuboring
2️⃣ Taklif qilingan tillardan maqsadli tilni tanlang
3️⃣ Chiroyli tarjimani oling

🌍 Mavjud tillar:
🇺🇿 Uzbek | 🇷🇺 Russian | 🇺🇸 English
🇰🇷 Korean | 🇹🇷 Turkish | 🇹🇯 Tajik

💎 Buyriqlar:
/start - Ishni boshla
/help - Bu yordam

✅ Tayormisiz? Matnni yuboring!"""
    await message.answer(text)


@router.message(TranslateStates.main_menu, F.text == "👇 Tilni tanlang (dan)")
async def select_source_language(message: Message, state: FSMContext):
    """Выбор исходного языка"""
    await state.set_state(TranslateStates.selecting_source_lang)
    await message.answer(
        "til tanlang menyusi",
        reply_markup=get_language_selection_keyboard()
    )


@router.message(TranslateStates.main_menu, F.text == "👇 Tilni tanlang (ga)")
async def select_target_language(message: Message, state: FSMContext):
    """Выбор целевого языка"""
    await state.set_state(TranslateStates.selecting_target_lang)
    await message.answer(
        "til tanlang menyusi",
        reply_markup=get_language_selection_keyboard()
    )


@router.message(TranslateStates.selecting_source_lang, F.text)
async def handle_source_lang_selection(message: Message, state: FSMContext):
    """Обработка выбора исходного языка"""
    user_id = message.from_user.id
    text = message.text.strip()
    
    if await db.is_banned(user_id):
        await message.answer(f"Siz bloklangan!")
        return
    
    if not any(flag in text for flag in ["🇷🇺", "🇺🇸", "🇰🇷", "🇹🇷", "🇹🇯", "🇺🇿"]):
        await message.answer("Iltimos, tilni tanlang!")
        return
    
    source_lang = lang_name_to_code(text)
    logger.info(f"Manba tili tanlandi: {text} -> {source_lang}")
    
    await state.update_data(source_lang=source_lang)
    await state.set_state(TranslateStates.main_menu)
    
    await message.answer(
        f"Tarjima tili tanlandi\n\n{text}",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(TranslateStates.selecting_target_lang, F.text)
async def handle_target_lang_selection(message: Message, state: FSMContext):
    """Обработка выбора целевого языка"""
    user_id = message.from_user.id
    text = message.text.strip()
    
    if await db.is_banned(user_id):
        await message.answer(f"Siz bloklangan!")
        return
    
    if not any(flag in text for flag in ["🇷🇺", "🇺🇸", "🇰🇷", "🇹🇷", "🇹🇯", "🇺🇿"]):
        await message.answer("Iltimos, tilni tanlang!")
        return
    
    target_lang = lang_name_to_code(text)
    logger.info(f"Maqsadli tili tanlandi: {text} -> {target_lang}")
    
    await state.update_data(target_lang=target_lang)
    await state.set_state(TranslateStates.main_menu)
    
    await message.answer(
        f"Tarjima tili tanlandi\n\n{text}",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(TranslateStates.main_menu, F.text)
async def handle_text_for_translation(message: Message, state: FSMContext):
    """Обработка текста для перевода"""
    user_id = message.from_user.id
    text = message.text.strip()
    
    if await db.is_banned(user_id):
        await message.answer(f"Siz bloklangan!")
        return
    
    if len(text) == 0 or len(text) > 5000:
        await message.answer(f"Matn 1 dan 5000 belgigacha bo'lishi kerak!")
        return
    
    data = await state.get_data()
    source_lang = data.get("source_lang", "auto")
    target_lang = data.get("target_lang", "uz")
    
    logger.info(f"Tarjima parametrlari: source_lang={source_lang}, target_lang={target_lang}, text={text[:50]}")
    
    await message.answer(f"Tarjima qilinmoqda...")
    
    translated = await Translator.translate(text, source_lang=source_lang, target_lang=target_lang)
    
    if translated:
        await db.add_translation(user_id, text, translated, source_lang, target_lang)
        
        await message.answer(translated, reply_markup=get_main_menu_keyboard())
    else:
        await message.answer(
            f"Tarjimada xato. Keyinroq qo'llab ko'ring.",
            reply_markup=get_main_menu_keyboard()
        )
