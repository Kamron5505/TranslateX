#!/usr/bin/env python3
"""
Диагностический скрипт для проверки работы бота
"""
import asyncio
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


async def diagnose():
    """Диагностика"""
    
    logger.info("=" * 60)
    logger.info("ДИАГНОСТИКА БОТА TranslateX")
    logger.info("=" * 60)
    
    # 1. Проверка конфигурации
    logger.info("\n1️⃣ ПРОВЕРКА КОНФИГУРАЦИИ")
    try:
        from config import BOT_TOKEN, ADMIN_IDS, DATABASE_PATH, LOG_LEVEL
        
        if not BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не установлен!")
            return False
        
        logger.info(f"✅ BOT_TOKEN: {BOT_TOKEN[:20]}...")
        logger.info(f"✅ ADMIN_IDS: {ADMIN_IDS}")
        logger.info(f"✅ DATABASE_PATH: {DATABASE_PATH}")
        logger.info(f"✅ LOG_LEVEL: {LOG_LEVEL}")
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке конфигурации: {e}")
        return False
    
    # 2. Проверка БД
    logger.info("\n2️⃣ ПРОВЕРКА БАЗЫ ДАННЫХ")
    try:
        from database import Database
        db = Database()
        await db.init()
        logger.info("✅ БД инициализирована")
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации БД: {e}")
        return False
    
    # 3. Проверка импортов
    logger.info("\n3️⃣ ПРОВЕРКА ИМПОРТОВ")
    try:
        from handlers import router, set_db
        from translator import Translator
        from keyboards import get_language_keyboard
        from states import TranslateStates, AdminStates
        logger.info("✅ Все импорты успешны")
    except Exception as e:
        logger.error(f"❌ Ошибка при импорте: {e}")
        return False
    
    # 4. Проверка подключения к Telegram API
    logger.info("\n4️⃣ ПРОВЕРКА ПОДКЛЮЧЕНИЯ К TELEGRAM API")
    try:
        from aiogram import Bot
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        logger.info(f"✅ Подключение успешно!")
        logger.info(f"   Бот: @{me.username}")
        logger.info(f"   ID: {me.id}")
        await bot.session.close()
    except Exception as e:
        logger.error(f"❌ Ошибка при подключении к Telegram: {e}")
        return False
    
    # 5. Проверка переводчика
    logger.info("\n5️⃣ ПРОВЕРКА ПЕРЕВОДЧИКА")
    try:
        result = await Translator.translate("Hello", source_lang="en", target_lang="ru")
        if result:
            logger.info(f"✅ Переводчик работает: 'Hello' → '{result}'")
        else:
            logger.warning("⚠️ Переводчик вернул None")
    except Exception as e:
        logger.error(f"❌ Ошибка при переводе: {e}")
        return False
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
    logger.info("=" * 60)
    logger.info("\nБот готов к запуску. Используйте: python main.py")
    
    return True


if __name__ == "__main__":
    result = asyncio.run(diagnose())
    sys.exit(0 if result else 1)
