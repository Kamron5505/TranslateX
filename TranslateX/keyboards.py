from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import LANGUAGES, EMOJI_PREMIUM, LANGUAGE_NAMES


def get_source_language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 Uzbek"), KeyboardButton(text="🇷🇺 Russian"), KeyboardButton(text="🇺🇸 English")],
            [KeyboardButton(text="🇰🇷 Korean"), KeyboardButton(text="🇹🇷 Turkish"), KeyboardButton(text="🇹🇯 Tajik")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_target_language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 Uzbek"), KeyboardButton(text="🇷🇺 Russian"), KeyboardButton(text="🇺🇸 English")],
            [KeyboardButton(text="🇰🇷 Korean"), KeyboardButton(text="🇹🇷 Turkish"), KeyboardButton(text="🇹🇯 Tajik")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_language_keyboard() -> ReplyKeyboardMarkup:
    return get_source_language_keyboard()


def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Tarjima qilish")],
            [KeyboardButton(text="🌍 Tilni tanlang")],
            [KeyboardButton(text="ℹ️ Yordam")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika")],
            [KeyboardButton(text="📢 Translyatsiya")],
            [KeyboardButton(text="🚫 Ban/Unban")],
            [KeyboardButton(text="◀️ Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ha", callback_data="confirm_yes"),
                InlineKeyboardButton(text="❌ Yo'q", callback_data="confirm_no")
            ]
        ]
    )


def lang_name_to_code(lang_name: str) -> str:
    """Преобразовать название языка в код"""
    # Извлекаем название из текста (например "🇰🇷 Korean" -> "Korean")
    parts = lang_name.split()
    if len(parts) > 1:
        lang_text = " ".join(parts[1:])  # Берем все после флага
    else:
        lang_text = lang_name
    
    lang_map = {
        "Uzbek": "uz",
        "Russian": "ru",
        "English": "en",
        "Korean": "ko",
        "Turkish": "tr",
        "Tajik": "tg",
    }
    
    # Ищем точное совпадение
    for key, code in lang_map.items():
        if key.lower() in lang_text.lower():
            return code
    
    # Если не нашли, возвращаем узбекский по умолчанию
    return "uz"
