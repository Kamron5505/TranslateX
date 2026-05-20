import logging
from typing import Optional
import asyncio
import aiohttp
import requests

logger = logging.getLogger(__name__)


class Translator:
    @staticmethod
    async def translate(text: str, source_lang: str = "auto", target_lang: str = "uz") -> Optional[str]:
        """
        Перевести текст используя MyMemory API или Google Translate
        
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
            
            # Для корейского используем Google Translate API
            if source_lang == "ko" or target_lang == "ko":
                return await Translator._translate_with_google(text, source_lang, target_lang)
            
            # Для остальных используем MyMemory API
            return await Translator._translate_with_mymemory(text, source_lang, target_lang)
            
        except Exception as e:
            logger.error(f"Tarjimada xato: {str(e)}")
            return None

    @staticmethod
    async def _translate_with_mymemory(text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Перевод через MyMemory API"""
        try:
            # Map language codes to language pairs for MyMemory
            lang_pairs = {
                ("auto", "uz"): "en|uz",
                ("uz", "ru"): "uz|ru",
                ("uz", "en"): "uz|en",
                ("uz", "ko"): "uz|ko",
                ("uz", "tr"): "uz|tr",
                ("uz", "tg"): "uz|tg",
                ("ru", "uz"): "ru|uz",
                ("ru", "en"): "ru|en",
                ("ru", "ko"): "ru|ko",
                ("ru", "tr"): "ru|tr",
                ("ru", "tg"): "ru|tg",
                ("en", "uz"): "en|uz",
                ("en", "ru"): "en|ru",
                ("en", "ko"): "en|ko",
                ("en", "tr"): "en|tr",
                ("en", "tg"): "en|tg",
                ("ko", "uz"): "ko|uz",
                ("ko", "ru"): "ko|ru",
                ("ko", "en"): "ko|en",
                ("ko", "tr"): "ko|tr",
                ("ko", "tg"): "ko|tg",
                ("tr", "uz"): "tr|uz",
                ("tr", "ru"): "tr|ru",
                ("tr", "en"): "tr|en",
                ("tr", "ko"): "tr|ko",
                ("tr", "tg"): "tr|tg",
                ("tg", "uz"): "tg|uz",
                ("tg", "ru"): "tg|ru",
                ("tg", "en"): "tg|en",
                ("tg", "ko"): "tg|ko",
                ("tg", "tr"): "tg|tr",
            }
            
            # Get language pair or use default
            lang_pair = lang_pairs.get((source_lang, target_lang), f"{source_lang}|{target_lang}")
            
            # Use MyMemory API
            url = "https://api.mymemory.translated.net/get"
            params = {
                "q": text,
                "langpair": lang_pair
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("responseStatus") == 200:
                            translated_text = data.get("responseData", {}).get("translatedText")
                            if translated_text:
                                logger.info(f"Tarjima muvaffaqiyatli (MyMemory): {source_lang} -> {target_lang}, Natija: {translated_text[:50]}")
                                return translated_text
            
            logger.error(f"MyMemory API xatosi: {source_lang} -> {target_lang}")
            return None
            
        except Exception as e:
            logger.error(f"MyMemory tarjimada xato: {str(e)}")
            return None

    @staticmethod
    async def _translate_with_google(text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Перевод через Google Translate API"""
        try:
            # Map language codes to Google Translate codes
            lang_map = {
                "uz": "uz",
                "ru": "ru",
                "en": "en",
                "ko": "ko",
                "tr": "tr",
                "tg": "tg",
                "auto": "auto"
            }
            
            src = lang_map.get(source_lang, source_lang)
            dest = lang_map.get(target_lang, target_lang)
            
            # Use Google Translate API via requests
            loop = asyncio.get_event_loop()
            
            def do_translate():
                url = "https://translate.googleapis.com/translate_a/element.js"
                params = {
                    "client": "gtx",
                    "sl": src,
                    "tl": dest,
                    "text": text
                }
                
                # Alternative: use simple Google Translate endpoint
                url = f"https://translate.googleapis.com/translate_a/single"
                params = {
                    "client": "gtx",
                    "sl": src,
                    "tl": dest,
                    "dt": "t",
                    "q": text
                }
                
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    # Parse the response - it's a complex JSON structure
                    import json
                    try:
                        data = response.json()
                        # Extract translated text from the response
                        if isinstance(data, list) and len(data) > 0:
                            if isinstance(data[0], list) and len(data[0]) > 0:
                                if isinstance(data[0][0], list) and len(data[0][0]) > 0:
                                    return data[0][0][0]
                    except:
                        pass
                
                return None
            
            translated_text = await loop.run_in_executor(None, do_translate)
            
            if translated_text:
                logger.info(f"Tarjima muvaffaqiyatli (Google): {source_lang} -> {target_lang}, Natija: {translated_text[:50]}")
                return translated_text
            
            logger.error(f"Google Translate xatosi: {source_lang} -> {target_lang}")
            return None
            
        except Exception as e:
            logger.error(f"Google Translate tarjimada xato: {str(e)}")
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
