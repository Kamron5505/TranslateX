from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import LANGUAGES, EMOJI_PREMIUM


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    buttons = []
    for emoji, code in LANGUAGES.items():
        buttons.append([
            InlineKeyboardButton(
                text=f"{emoji}",
                callback_data=f"lang_{code}"
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
