from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import LANGUAGES, EMOJI_PREMIUM


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка с флагами"""
    buttons = []
    
    # Порядок языков
    lang_order = [
        ("ru", "🇷🇺"),
        ("en", "🇺🇸"),
        ("pt", "🇵🇹"),
        ("de", "🇩🇪"),
        ("fr", "🇫🇷"),
        ("es", "🇪🇸"),
        ("it", "🇮🇹"),
        ("tr", "🇹🇷"),
        ("uz", "🇺🇿"),
    ]
    
    # Создаем кнопки по 3 в ряду
    for i in range(0, len(lang_order), 3):
        row = []
        for j in range(3):
            if i + j < len(lang_order):
                code, emoji = lang_order[i + j]
                row.append(
                    InlineKeyboardButton(
                        text=emoji,
                        callback_data=f"lang_{code}"
                    )
                )
        if row:
            buttons.append(row)
    
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
