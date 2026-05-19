from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import LANGUAGES, EMOJI_PREMIUM


def get_language_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура выбора языка с Reply Keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Tilni tanlang (ru)"), KeyboardButton(text="🇺🇸 Tilni tanlang (en)")],
            [KeyboardButton(text="🇵🇹 Tilni tanlang (pt)"), KeyboardButton(text="🇩🇪 Tilni tanlang (de)")],
            [KeyboardButton(text="🇫🇷 Tilni tanlang (fr)"), KeyboardButton(text="🇪🇸 Tilni tanlang (es)")],
            [KeyboardButton(text="🇮🇹 Tilni tanlang (it)"), KeyboardButton(text="🇹🇷 Tilni tanlang (tr)")],
            [KeyboardButton(text="🇺🇿 Tilni tanlang (uz)")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


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
