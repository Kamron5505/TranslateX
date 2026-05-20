import logging
from typing import Optional
import asyncio
import aiohttp

logger = logging.getLogger(__name__)


class Translator:
    @staticmethod
    async def translate(text: str, source_lang: str = "auto", target_lang: str = "uz") -> Optional[str]:
        """
        Перевести текст используя MyMemory API (более надежный для всех языков)
        
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
            
            logger.info(f"Tarjima: {source_lang} -> {target_lang}, Matn: {text[:50]}")
            
            # Map language codes to language pairs for MyMemory
            lang_pairs = {
                ("auto", "uz"): "en|uz",
                ("uz", "ru"): "uz|ru",
                ("uz", "en"): "uz|en",
                ("ru", "uz"): "ru|uz",
                ("ru", "en"): "ru|en",
                ("en", "uz"): "en|uz",
                ("en", "ru"): "en|ru",
                ("fr", "ru"): "fr|ru",
                ("fr", "en"): "fr|en",
                ("fr", "uz"): "fr|uz",
                ("de", "ru"): "de|ru",
                ("de", "en"): "de|en",
                ("de", "uz"): "de|uz",
                ("pt", "ru"): "pt|ru",
                ("pt", "en"): "pt|en",
                ("pt", "uz"): "pt|uz",
                ("it", "ru"): "it|ru",
                ("it", "en"): "it|en",
                ("it", "uz"): "it|uz",
                ("tr", "ru"): "tr|ru",
                ("tr", "en"): "tr|en",
                ("tr", "uz"): "tr|uz",
                ("es", "ru"): "es|ru",
                ("es", "en"): "es|en",
                ("es", "uz"): "es|uz",
            }
            
            # Get language pair or use default
            lang_pair = lang_pairs.get((source_lang, target_lang), f"{source_lang}|{target_lang}")
            
            # Use MyMemory API
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": lang_pair
            }
            
            loop = asyncio.get_event_loop()
            
            async def fetch_translation():
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get("responseStatus") == 200:
                                return data.get("responseData", {}).get("translatedText")
                return None
            
            translated_text = await fetch_translation()
            
            if translated_text:
                logger.info(f"Tarjima muvaffaqiyatli: {source_lang} -> {target_lang}, Natija: {translated_text[:50]}")
                return translated_text
            else:
                logger.error(f"MyMemory API xatosi: {source_lang} -> {target_lang}")
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
