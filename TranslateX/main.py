import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
from dotenv import load_dotenv

from config import BOT_TOKEN, LOG_LEVEL, DATABASE_PATH, EMOJI_PREMIUM
from database import Database
from handlers import router, set_db

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация БД
db = Database()


async def set_commands(bot: Bot):
    """Установить команды бота"""
    commands = [
        BotCommand(command="start", description="Botni ishga tushurish"),
        BotCommand(command="help", description="Yordam olish"),
        BotCommand(command="admin", description="Admin paneli"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    logger.info("✅ Buyriqlar o'rnatildi")


async def set_menu_button(bot: Bot):
    """Установить кнопку меню"""
    menu_button = MenuButtonCommands()
    await bot.set_chat_menu_button(menu_button=menu_button)
    logger.info("✅ Menu tugmasi o'rnatildi")


async def main():
    """Главная функция"""
    
    # Проверка токена
    if not BOT_TOKEN:
        logger.error(f"{EMOJI_PREMIUM['error']} BOT_TOKEN не установлен в .env файле!")
        return
    
    # Создание директории для БД
    os.makedirs(os.path.dirname(DATABASE_PATH) or ".", exist_ok=True)
    
    # Инициализация БД
    await db.init()
    
    # Передаем БД в handlers
    set_db(db)
    
    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Установка команд
    await set_commands(bot)
    
    # Установка кнопки меню
    await set_menu_button(bot)
    
    # Подключение роутера
    dp.include_router(router)
    
    logger.info(f"{EMOJI_PREMIUM['start']} TranslateX boti ishga tushdi!")
    logger.info(f"{EMOJI_PREMIUM['diamond']} Versiya: 1.0.0")
    logger.info(f"{EMOJI_PREMIUM['lightning']} Xabarlarni kutmoqda...")
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info(f"{EMOJI_PREMIUM['error']} Bot to'xtatildi")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

