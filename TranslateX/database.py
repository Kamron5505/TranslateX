import aiosqlite
import logging
from datetime import datetime
from config import DATABASE_PATH

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path

    async def init(self):
        """Инициализация базы данных"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    language TEXT DEFAULT 'uz',
                    translations_count INTEGER DEFAULT 0,
                    is_banned INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    source_text TEXT,
                    translated_text TEXT,
                    source_lang TEXT,
                    target_lang TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS spam_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
            logger.info("✅ База данных инициализирована")

    async def add_user(self, user_id: int, username: str, first_name: str):
        """Добавить пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT OR IGNORE INTO users (user_id, username, first_name) 
                   VALUES (?, ?, ?)""",
                (user_id, username, first_name)
            )
            await db.commit()

    async def get_user(self, user_id: int):
        """Получить пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT * FROM users WHERE user_id = ?",
                (user_id,)
            )
            return await cursor.fetchone()

    async def set_language(self, user_id: int, language: str):
        """Установить язык пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET language = ? WHERE user_id = ?",
                (language, user_id)
            )
            await db.commit()

    async def get_language(self, user_id: int) -> str:
        """Получить язык пользователя"""
        user = await self.get_user(user_id)
        return user[3] if user else "uz"

    async def add_translation(self, user_id: int, source_text: str, 
                             translated_text: str, source_lang: str, target_lang: str):
        """Добавить перевод в историю"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """INSERT INTO translations 
                   (user_id, source_text, translated_text, source_lang, target_lang)
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, source_text, translated_text, source_lang, target_lang)
            )
            await db.execute(
                """UPDATE users SET translations_count = translations_count + 1,
                   last_used = CURRENT_TIMESTAMP WHERE user_id = ?""",
                (user_id,)
            )
            await db.commit()

    async def get_stats(self):
        """Получить статистику"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM users WHERE is_banned = 0")
            total_users = (await cursor.fetchone())[0]
            
            cursor = await db.execute("SELECT SUM(translations_count) FROM users")
            total_translations = (await cursor.fetchone())[0] or 0
            
            cursor = await db.execute("SELECT COUNT(*) FROM users WHERE is_banned = 1")
            banned_users = (await cursor.fetchone())[0]
            
            return {
                "total_users": total_users,
                "total_translations": total_translations,
                "banned_users": banned_users
            }

    async def ban_user(self, user_id: int):
        """Забанить пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET is_banned = 1 WHERE user_id = ?",
                (user_id,)
            )
            await db.commit()

    async def unban_user(self, user_id: int):
        """Разбанить пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET is_banned = 0 WHERE user_id = ?",
                (user_id,)
            )
            await db.commit()

    async def is_banned(self, user_id: int) -> bool:
        """Проверить забанен ли пользователь"""
        user = await self.get_user(user_id)
        return user[6] == 1 if user else False

    async def get_all_users(self):
        """Получить всех пользователей"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT user_id FROM users WHERE is_banned = 0")
            return await cursor.fetchall()

    async def log_spam(self, user_id: int, action: str):
        """Логировать спам"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO spam_log (user_id, action) VALUES (?, ?)",
                (user_id, action)
            )
            await db.commit()

    async def get_spam_count(self, user_id: int, minutes: int = 5) -> int:
        """Получить количество действий за последние N минут"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """SELECT COUNT(*) FROM spam_log 
                   WHERE user_id = ? AND timestamp > datetime('now', '-' || ? || ' minutes')""",
                (user_id, minutes)
            )
            return (await cursor.fetchone())[0]
