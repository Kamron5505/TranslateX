import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/bot.db")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LANGUAGES = {
    "🇷🇺": "ru",
    "🇺🇸": "en",
    "🇵🇹": "pt",
    "🇩🇪": "de",
    "🇫🇷": "fr",
    "🇪🇸": "es",
    "🇮🇹": "it",
    "🇹🇷": "tr",
    "🇺🇿": "uz",
}

LANGUAGE_NAMES = {
    "ru": "Русский",
    "en": "English",
    "pt": "Português",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "it": "Italiano",
    "tr": "Türkçe",
    "uz": "Ўзбек",
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
