from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import LANGUAGES, EMOJI_PREMIUM, LANGUAGE_NAMES


def get_source_language_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора исходного языка"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 Uzbek"), KeyboardButton(text="🇷🇺 Russian"), KeyboardButton(text="🇺🇸 English"), KeyboardButton(text="🇹🇷 Türkçe")],
            [KeyboardButton(text="🇵🇹 Qozoq"), KeyboardButton(text="🇩🇪 Tojik"), KeyboardButton(text="🇫🇷 Qirg'iz"), KeyboardButton(text="🇮🇹 Arabic")],
            [KeyboardButton(text="🇮🇷 Iran"), KeyboardButton(text="🇯🇵 Japan"), KeyboardButton(text="🇰🇷 Korean"), KeyboardButton(text="🇪🇸 Spanish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_target_language_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора целевого языка"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 Uzbek"), KeyboardButton(text="🇷🇺 Russian"), KeyboardButton(text="🇺🇸 English"), KeyboardButton(text="🇹🇷 Türkçe")],
            [KeyboardButton(text="🇵🇹 Qozoq"), KeyboardButton(text="🇩🇪 Tojik"), KeyboardButton(text="🇫🇷 Qirg'iz"), KeyboardButton(text="🇮🇹 Arabic")],
            [KeyboardButton(text="🇮🇷 Iran"), KeyboardButton(text="🇯🇵 Japan"), KeyboardButton(text="🇰🇷 Korean"), KeyboardButton(text="🇪🇸 Spanish")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_language_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора языка (для совместимости)"""
    return get_source_language_keyboard()


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Асосий клавиатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{EMOJI_PREMIUM['translate']} Тарғима қилиш")],
            [KeyboardButton(text=f"{EMOJI_PREMIUM['world']} Тилни танланг")],
            [KeyboardButton(text=f"{EMOJI_PREMIUM['info']} Ёрдам")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Админ клавиатура"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"{EMOJI_PREMIUM['stats']} Статистика")],
            [KeyboardButton(text=f"{EMOJI_PREMIUM['broadcast']} Трансляция")],
            [KeyboardButton(text=f"{EMOJI_PREMIUM['ban']} Бан/Разбан")],
            [KeyboardButton(text="◀️ Орқага")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{EMOJI_PREMIUM['success']} Ҳа", callback_data="confirm_yes"),
                InlineKeyboardButton(text=f"{EMOJI_PREMIUM['error']} Йўқ", callback_data="confirm_no")
            ]
        ]
    )


def lang_name_to_code(lang_name: str) -> str:
    """Преобразовать название языка в код"""
    lang_map = {
        "Uzbek": "uz",
        "Russian": "ru",
        "English": "en",
        "Türkçe": "tr",
        "Qozoq": "pt",
        "Tojik": "de",
        "Qirg'iz": "fr",
        "Arabic": "it",
        "Iran": "fa",
        "Japan": "ja",
        "Korean": "ko",
        "Spanish": "es",
    }
    
    # Извлекаем название из текста (например "🇷🇺 Russian" -> "Russian")
    for key, code in lang_map.items():
        if key in lang_name:
            return code
    
    return "uz"  # По умолчанию узбекский
