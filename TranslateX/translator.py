import logging
from deep_translator import GoogleTranslator
from typing import Optional

logger = logging.getLogger(__name__)

# Правильные коды языков для Google Translate
GOOGLE_LANG_CODES = {
    "uz": "uz",      # Uzbek
    "ru": "ru",      # Russian
    "en": "en",      # English
    "pt": "pt",      # Portuguese
    "de": "de",      # German
    "fr": "fr",      # French
    "es": "es",      # Spanish
    "it": "it",      # Italian
    "tr": "tr",      # Turkish
}


class Translator:
    @staticmethod
    async def translate(text: str, source_lang: str = "auto", target_lang: str = "uz") -> Optional[str]:
        """
        Перевести текст используя Google Translate
        
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
            
            # Преобразуем коды языков для Google Translate
            google_target = GOOGLE_LANG_CODES.get(target_lang, target_lang)
            google_source = source_lang if source_lang == "auto" else GOOGLE_LANG_CODES.get(source_lang, source_lang)
            
            logger.info(f"Tarjima: {google_source} -> {google_target}, Matn: {text[:50]}")
            
            translator = GoogleTranslator(source_language=google_source, target_language=google_target)
            result = translator.translate(text)
            
            logger.info(f"Tarjima muvaffaqiyatli: {source_lang} -> {target_lang}, Natija: {result[:50]}")
            return result
            
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
