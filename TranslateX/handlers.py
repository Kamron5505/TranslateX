import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime

from config import EMOJI_PREMIUM, LANGUAGES, LANGUAGE_NAMES, ADMIN_IDS
from database import Database
from translator import Translator
from keyboards import (
    get_language_keyboard, get_main_keyboard, get_admin_keyboard, get_confirm_keyboard,
    get_source_language_keyboard, get_target_language_keyboard, lang_name_to_code
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
    
    text = f"Assalomu Aleykum! {EMOJI_PREMIUM['start']}\n\nSiz aktiv xolatdasiz {EMOJI_PREMIUM['world']}\n\nQuydagi menyudan tilni sozlab oling!"
    
    await message.answer(text, reply_markup=get_source_language_keyboard())
    await state.clear()


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = f"""ℹ️ YORDAM - TranslateX

⚡ Asosiy funktsiyalar:

1️⃣ Tarjima qilish uchun matnni yuboring
2️⃣ Taklif qilingan tillardan maqsadli tilni tanlang
3️⃣ Chiroyli tarjimani oling {EMOJI_PREMIUM['magic']}

🌍 Mavjud tillar:
🇺🇿 Uzbek | 🇷🇺 Russian | 🇺🇸 English | 🇹🇷 Turkish
🇵🇹 Portuguese | 🇩🇪 German | 🇫🇷 French | 🇮🇹 Italian

💎 Buyriqlar:
/start - Ishni boshla
/help - Bu yordam

✅ Tayormisiz? Matnni yuboring!"""
    await message.answer(text)


@router.message(StateFilter(None), F.text)
async def handle_source_language(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if await db.is_banned(user_id):
        await message.answer(f"{EMOJI_PREMIUM['error']} Siz bloklangan!")
        return
    
    # Проверяем если это выбор языка (содержит флаг)
    if any(flag in text for flag in ["🇷🇺", "🇺🇸", "🇵🇹", "🇩🇪", "🇫🇷", "🇪🇸", "🇮🇹", "🇹🇷", "🇺🇿"]):
        source_lang = lang_name_to_code(text)
        logger.info(f"Manba tili tanlandi: {text} -> {source_lang}")
        await state.update_data(source_lang=source_lang)
        await state.set_state(TranslateStates.waiting_for_text)
        
        await message.answer(f"{EMOJI_PREMIUM['translate']} Matnni yuboring:")
        return
    
    spam_count = await db.get_spam_count(user_id, minutes=1)
    if spam_count > 10:
        await db.log_spam(user_id, "spam_detected")
        await message.answer(f"{EMOJI_PREMIUM['error']} Juda ko'p so'rovlar! Kuting...")
        return
    
    await db.log_spam(user_id, "translate_request")
    
    if len(text) == 0 or len(text) > 5000:
        await message.answer(f"{EMOJI_PREMIUM['error']} Matn 1 dan 5000 belgigacha bo'lishi kerak!")
        return
    
    await state.update_data(source_text=text)
    await state.set_state(TranslateStates.waiting_for_target_lang)
    
    await message.answer(
        f"{EMOJI_PREMIUM['world']} Matn qaysi tilga tarjima qilinsin?",
        reply_markup=get_target_language_keyboard()
    )


@router.message(TranslateStates.waiting_for_text, F.text)
async def handle_text_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if await db.is_banned(user_id):
        await message.answer(f"{EMOJI_PREMIUM['error']} Siz bloklangan!")
        await state.clear()
        return
    
    if len(text) == 0 or len(text) > 5000:
        await message.answer(f"{EMOJI_PREMIUM['error']} Matn 1 dan 5000 belgigacha bo'lishi kerak!")
        return
    
    await state.update_data(source_text=text)
    await state.set_state(TranslateStates.waiting_for_target_lang)
    
    await message.answer(
        f"{EMOJI_PREMIUM['world']} Matn qaysi tilga tarjima qilinsin?",
        reply_markup=get_target_language_keyboard()
    )


@router.message(TranslateStates.waiting_for_target_lang, F.text)
async def handle_target_lang_selection(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if await db.is_banned(user_id):
        await message.answer(f"{EMOJI_PREMIUM['error']} Siz bloklangan!")
        await state.clear()
        return
    
    if not any(flag in text for flag in ["🇷🇺", "🇺🇸", "🇵🇹", "🇩🇪", "🇫🇷", "🇪🇸", "🇮🇹", "🇹🇷", "🇺🇿"]):
        await message.answer(f"{EMOJI_PREMIUM['error']} Iltimos, tilni tanlang!")
        return
    
    target_lang = lang_name_to_code(text)
    logger.info(f"Maqsadli tili tanlandi: {text} -> {target_lang}")
    
    data = await state.get_data()
    source_text = data.get("source_text", "")
    source_lang = data.get("source_lang", "auto")
    
    logger.info(f"Tarjima parametrlari: source_lang={source_lang}, target_lang={target_lang}, text={source_text[:50]}")
    
    await message.answer(f"{EMOJI_PREMIUM['lightning']} Tarjima qilinmoqda...")
    
    translated = await Translator.translate(source_text, source_lang=source_lang, target_lang=target_lang)
    
    if translated:
        await db.add_translation(user_id, source_text, translated, source_lang, target_lang)
        
        target_lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        source_lang_name = LANGUAGE_NAMES.get(source_lang, source_lang)
        
        result_text = f"{EMOJI_PREMIUM['success']} Tarjima tayyor!\n\n{EMOJI_PREMIUM['world']} Manba tili: {source_lang_name}\n{EMOJI_PREMIUM['world']} Tarjima tili: {target_lang_name}\n\n📝 Natija: {translated}\n\n{EMOJI_PREMIUM['start']} Yana matn yuboring!"
        
        await message.answer(result_text, reply_markup=get_source_language_keyboard())
    else:
        await message.answer(
            f"{EMOJI_PREMIUM['error']} Tarjimada xato. Keyinroq qo'llab ko'ring.",
            reply_markup=get_source_language_keyboard()
        )
    
    await state.clear()
