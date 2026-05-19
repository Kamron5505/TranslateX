import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS = list(map(int, ADMIN_IDS_STR.split(","))) if ADMIN_IDS_STR else []
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bot.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LANGUAGES = {
    "🇺🇿": "uz",
    "🇷🇺": "ru",
    "🇺🇸": "en",
    "🇵🇹": "pt",
    "🇩🇪": "de",
    "🇫🇷": "fr",
    "🇪🇸": "es",
    "🇮🇹": "it",
    "🇹🇷": "tr",
}

LANGUAGE_NAMES = {
    "uz": "Uzbek",
    "ru": "Russian",
    "en": "English",
    "pt": "Portuguese",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "tr": "Turkish",
}

EMOJI_PREMIUM = {
    "start": "✨",
    "translate": "🚀",
    "diamond": "💎",
    "world": "🌍",
    "lightning": "⚡",
    "magic": "🪄",
    "success": "✅",
    "error": "❌",
    "info": "ℹ️",
    "stats": "📊",
    "users": "👥",
    "ban": "🚫",
    "unban": "✔️",
    "broadcast": "📢",
}

