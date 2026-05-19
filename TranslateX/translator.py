import logging
import aiohttp
from typing import Optional

logger = logging.getLogger(__name__)

# LibreTranslate API endpoint
LIBRETRANSLATE_API = "https://libretranslate.com/translate"

# Маппинг кодов языков для LibreTranslate
LIBRETRANSLATE_LANG_CODES = {
    "uz": "uz",
    "ru": "ru",
    "en": "en",
    "pt": "pt",
    "de": "de",
    "fr": "fr",
    "es": "es",
    "it": "it",
    "tr": "tr",
}


class Translator:
    @staticmethod
    async def translate(text: str, source_lang: str = "auto", target_lang: str = "uz") -> Optional[str]:
        """
        Перевести текст используя LibreTranslate API
        
        Args:
            text: Текст для перевода
            source_lang: Исходный язык (auto для автоопределения)
            target_lang: Целевой язык
            
        Returns:
            Переведенный текст или None при ошибке
        """
        try:
            if not text or len(text.strip()) == 0:
                return None
            
            if len(text) > 5000:
                text = text[:5000]
            
            # Преобразуем коды языков для LibreTranslate
            target_code = LIBRETRANSLATE_LANG_CODES.get(target_lang, target_lang)
            source_code = source_lang if source_lang == "auto" else LIBRETRANSLATE_LANG_CODES.get(source_lang, source_lang)
            
            payload = {
                "q": text,
                "source": source_code,
                "target": target_code
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(LIBRETRANSLATE_API, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        result = data.get("translatedText")
                        logger.info(f"Tarjima muvaffaqiyatli: {source_lang} → {target_lang}")
                        return result
                    else:
                        logger.error(f"LibreTranslate API xatosi: {response.status}")
                        return None
            
        except Exception as e:
            logger.error(f"Tarjimada xato: {str(e)}")
            return None

    @staticmethod
    def get_language_code(emoji: str) -> Optional[str]:
        """Получить код языка по emoji"""
        from config import LANGUAGES
        return LANGUAGES.get(emoji)

    @staticmethod
    def get_language_name(code: str) -> str:
        """Получить название языка по коду"""
        from config import LANGUAGE_NAMES
        return LANGUAGE_NAMES.get(code, code)
