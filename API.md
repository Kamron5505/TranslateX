# 📖 API Документация TranslateX

## Модули и функции

### 1. config.py

Конфигурация и константы приложения.

#### Переменные

```python
BOT_TOKEN: str              # Токен Telegram бота
ADMIN_IDS: List[int]        # Список ID администраторов
DATABASE_PATH: str          # Путь к БД
LOG_LEVEL: str              # Уровень логирования

LANGUAGES: Dict[str, str]   # Словарь emoji -> код языка
LANGUAGE_NAMES: Dict[str, str]  # Словарь код -> название
EMOJI_PREMIUM: Dict[str, str]   # Premium emoji
```

#### Пример использования

```python
from config import BOT_TOKEN, ADMIN_IDS, LANGUAGES

print(BOT_TOKEN)  # Токен бота
print(ADMIN_IDS)  # [123456789, 987654321]
print(LANGUAGES)  # {'🇷🇺': 'ru', '🇺🇸': 'en', ...}
```

---

### 2. database.py

Работа с SQLite базой данных.

#### Класс Database

```python
class Database:
    def __init__(self, db_path: str = DATABASE_PATH)
    async def init()
    async def add_user(user_id: int, username: str, first_name: str)
    async def get_user(user_id: int)
    async def set_language(user_id: int, language: str)
    async def get_language(user_id: int) -> str
    async def add_translation(user_id: int, source_text: str, 
                             translated_text: str, source_lang: str, target_lang: str)
    async def get_stats() -> Dict
    async def ban_user(user_id: int)
    async def unban_user(user_id: int)
    async def is_banned(user_id: int) -> bool
    async def get_all_users() -> List
    async def log_spam(user_id: int, action: str)
    async def get_spam_count(user_id: int, minutes: int = 5) -> int
```

#### Примеры использования

```python
from database import Database

db = Database()

# Инициализация БД
await db.init()

# Добавить пользователя
await db.add_user(123456, "john_doe", "John")

# Получить пользователя
user = await db.get_user(123456)

# Установить язык
await db.set_language(123456, "ru")

# Получить язык
lang = await db.get_language(123456)

# Добавить перевод
await db.add_translation(123456, "Hello", "Привет", "auto", "ru")

# Получить статистику
stats = await db.get_stats()
# {'total_users': 42, 'total_translations': 156, 'banned_users': 2}

# Забанить пользователя
await db.ban_user(123456)

# Разбанить пользователя
await db.unban_user(123456)

# Проверить бан
is_banned = await db.is_banned(123456)

# Получить всех пользователей
users = await db.get_all_users()

# Логировать спам
await db.log_spam(123456, "spam_detected")

# Получить количество спама за 5 минут
spam_count = await db.get_spam_count(123456, minutes=5)
```

---

### 3. translator.py

Логика перевода текстов.

#### Класс Translator

```python
class Translator:
    @staticmethod
    async def translate(text: str, source_lang: str = "auto", 
                       target_lang: str = "uz") -> Optional[str]
    
    @staticmethod
    def get_language_code(emoji: str) -> Optional[str]
    
    @staticmethod
    def get_language_name(code: str) -> str
```

#### Примеры использования

```python
from translator import Translator

# Перевести текст
result = await Translator.translate("Hello", source_lang="auto", target_lang="ru")
# "Привет"

# Получить код языка по emoji
code = Translator.get_language_code("🇷🇺")
# "ru"

# Получить название языка
name = Translator.get_language_name("ru")
# "Русский"
```

---

### 4. keyboards.py

Клавиатуры и кнопки для интерфейса.

#### Функции

```python
def get_language_keyboard() -> InlineKeyboardMarkup
def get_main_keyboard() -> ReplyKeyboardMarkup
def get_admin_keyboard() -> ReplyKeyboardMarkup
def get_confirm_keyboard() -> InlineKeyboardMarkup
```

#### Примеры использования

```python
from keyboards import get_language_keyboard, get_main_keyboard

# Клавиатура выбора языка
kb = get_language_keyboard()
await message.answer("Выберите язык:", reply_markup=kb)

# Главная клавиатура
kb = get_main_keyboard()
await message.answer("Главное меню:", reply_markup=kb)
```

---

### 5. states.py

FSM состояния для управления диалогом.

#### Классы состояний

```python
class TranslateStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_language = State()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_ban_user_id = State()
    waiting_for_unban_user_id = State()
    confirm_broadcast = State()
```

#### Примеры использования

```python
from states import TranslateStates, AdminStates

# Установить состояние
await state.set_state(TranslateStates.waiting_for_text)

# Получить состояние
current_state = await state.get_state()

# Очистить состояние
await state.clear()

# Обновить данные состояния
await state.update_data(source_text="Hello")

# Получить данные состояния
data = await state.get_data()
text = data.get("source_text")
```

---

### 6. handlers.py

Обработчики команд и сообщений.

#### Команды

```python
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext)

@router.message(Command("help"))
async def cmd_help(message: Message)

@router.message(Command("admin"))
async def cmd_admin(message: Message)
```

#### Обработчики текста

```python
@router.message(StateFilter(None), F.text)
async def handle_text(message: Message, state: FSMContext)

@router.callback_query(TranslateStates.waiting_for_language, F.data.startswith("lang_"))
async def handle_language_selection(callback: CallbackQuery, state: FSMContext)
```

#### Админ функции

```python
@router.message(F.text.contains("Статистика"))
async def admin_stats(message: Message)

@router.message(F.text.contains("Рассылка"))
async def admin_broadcast_start(message: Message, state: FSMContext)

@router.message(F.text.contains("Бан"))
async def admin_ban_start(message: Message, state: FSMContext)
```

---

### 7. main.py

Главный файл запуска приложения.

#### Функция main

```python
async def main()
```

Инициализирует бота, БД и запускает polling.

#### Пример использования

```bash
python main.py
```

---

## Структура данных

### User объект

```python
{
    "user_id": 123456,
    "username": "john_doe",
    "first_name": "John",
    "language": "ru",
    "translations_count": 5,
    "is_banned": 0,
    "created_at": "2026-05-18 22:30:45",
    "last_used": "2026-05-18 22:35:12"
}
```

### Translation объект

```python
{
    "id": 1,
    "user_id": 123456,
    "source_text": "Hello",
    "translated_text": "Привет",
    "source_lang": "auto",
    "target_lang": "ru",
    "created_at": "2026-05-18 22:30:45"
}
```

### Stats объект

```python
{
    "total_users": 42,
    "total_translations": 156,
    "banned_users": 2
}
```

---

## Обработка ошибок

### Исключения

```python
# Ошибка перевода
try:
    result = await Translator.translate(text)
except Exception as e:
    logger.error(f"Ошибка перевода: {str(e)}")
    return None

# Ошибка БД
try:
    await db.add_user(user_id, username, first_name)
except Exception as e:
    logger.error(f"Ошибка БД: {str(e)}")
```

---

## Логирование

### Уровни логирования

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Отладочная информация")
logger.info("✅ Информационное сообщение")
logger.warning("⚠️ Предупреждение")
logger.error("❌ Ошибка")
logger.critical("🔴 Критическая ошибка")
```

---

## Асинхронное программирование

### Async/Await

```python
# Асинхронная функция
async def my_async_function():
    result = await some_async_operation()
    return result

# Вызов асинхронной функции
result = await my_async_function()

# Параллельное выполнение
results = await asyncio.gather(
    async_func1(),
    async_func2(),
    async_func3()
)
```

---

## Фильтры и обработчики

### Фильтры

```python
from aiogram.filters import Command, StateFilter
from aiogram.types import F

# Фильтр команды
@router.message(Command("start"))

# Фильтр состояния
@router.message(StateFilter(None))

# Фильтр текста
@router.message(F.text)

# Фильтр содержимого
@router.message(F.text.contains("Hello"))

# Фильтр callback_query
@router.callback_query(F.data.startswith("lang_"))
```

---

## Примеры интеграции

### Добавление нового языка

```python
# 1. Добавить в config.py
LANGUAGES = {
    ...
    "🇯🇵": "ja",  # Новый язык
}

LANGUAGE_NAMES = {
    ...
    "ja": "日本語",
}

# 2. Клавиатура автоматически обновится
```

### Добавление новой команды

```python
# В handlers.py
@router.message(Command("mycommand"))
async def cmd_mycommand(message: Message):
    await message.answer("Ответ на команду")
```

### Добавление нового состояния

```python
# В states.py
class MyStates(StatesGroup):
    my_state = State()

# В handlers.py
@router.message(MyStates.my_state)
async def handle_my_state(message: Message, state: FSMContext):
    await state.clear()
```

---

## Производительность

### Оптимизация

- Используйте асинхронные операции
- Кэшируйте часто используемые данные
- Ограничивайте размер текста (5000 символов)
- Используйте антиспам систему

### Масштабирование

- Используйте Redis для кэширования
- Используйте PostgreSQL вместо SQLite для больших объемов
- Используйте очереди задач (Celery)

---

## Безопасность

### Проверки

- Проверка прав администратора
- Проверка бана пользователя
- Валидация входных данных
- Логирование всех действий

### Best Practices

- Никогда не логируйте токены
- Используйте переменные окружения
- Валидируйте все входные данные
- Используйте HTTPS для API

---

**Документация полная и готова к использованию!** ✨
