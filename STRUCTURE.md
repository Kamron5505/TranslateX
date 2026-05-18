# 📁 Структура проекта TranslateX

## Полная структура файлов

```
TranslateX/
│
├── 📄 main.py                    # Точка входа приложения
│   └── Инициализирует бота, БД и запускает polling
│
├── 📄 config.py                  # Конфигурация и константы
│   ├── BOT_TOKEN, ADMIN_IDS
│   ├── LANGUAGES (emoji -> код)
│   ├── LANGUAGE_NAMES (код -> название)
│   └── EMOJI_PREMIUM (красивые emoji)
│
├── 📄 database.py                # Работа с SQLite БД
│   ├── Класс Database
│   ├── Таблица users
│   ├── Таблица translations
│   └── Таблица spam_log
│
├── 📄 translator.py              # Логика перевода
│   ├── Класс Translator
│   ├── translate() - перевод текста
│   ├── get_language_code() - код по emoji
│   └── get_language_name() - название по коду
│
├── 📄 keyboards.py               # UI клавиатуры и кнопки
│   ├── get_language_keyboard() - выбор языка
│   ├── get_main_keyboard() - главное меню
│   ├── get_admin_keyboard() - админ панель
│   └── get_confirm_keyboard() - подтверждение
│
├── 📄 states.py                  # FSM состояния
│   ├── TranslateStates
│   │   ├── waiting_for_text
│   │   └── waiting_for_language
│   └── AdminStates
│       ├── waiting_for_broadcast
│       ├── waiting_for_ban_user_id
│       ├── waiting_for_unban_user_id
│       └── confirm_broadcast
│
├── 📄 handlers.py                # Обработчики команд и сообщений
│   ├── Команды (/start, /help, /admin)
│   ├── Обработка текста
│   ├── Выбор языка
│   ├── Админ функции
│   │   ├── Статистика
│   │   ├── Рассылка
│   │   ├── Бан/Разбан
│   │   └── Логирование
│   └── Обработка ошибок
│
├── 📄 requirements.txt            # Зависимости проекта
│   ├── aiogram==3.3.0
│   ├── python-dotenv==1.0.0
│   ├── aiohttp==3.9.1
│   ├── deep-translator==1.11.4
│   └── aiosqlite==0.19.0
│
├── 📄 .env                        # Переменные окружения (не коммитить!)
│   ├── BOT_TOKEN
│   ├── ADMIN_IDS
│   ├── DATABASE_PATH
│   └── LOG_LEVEL
│
├── 📄 .env.example                # Пример .env файла
│
├── 📁 data/                       # Директория для БД (создается автоматически)
│   └── bot.db                     # SQLite база данных
│
├── 📁 logs/                       # Директория для логов (опционально)
│   └── bot.log                    # Логи приложения
│
├── 📁 __pycache__/                # Кэш Python (игнорировать)
│
├── 📚 ДОКУМЕНТАЦИЯ
│   ├── README.md                  # Основная документация
│   ├── SETUP.md                   # Инструкция установки
│   ├── EXAMPLES.md                # Примеры использования
│   ├── API.md                     # API документация
│   ├── DEPLOYMENT.md              # Развертывание
│   ├── PROJECT_INFO.md            # Информация о проекте
│   ├── FAQ.md                     # Часто задаваемые вопросы
│   └── STRUCTURE.md               # Этот файл
│
└── 🐳 DOCKER (опционально)
    ├── Dockerfile                 # Docker образ
    └── docker-compose.yml         # Docker Compose конфигурация
```

## Описание каждого файла

### Основные файлы приложения

#### main.py (1.9 KB)
```python
# Главный файл запуска
# Функции:
# - Загрузка конфигурации
# - Инициализация БД
# - Создание бота и диспетчера
# - Запуск polling
```

#### config.py (1.1 KB)
```python
# Конфигурация приложения
# Содержит:
# - BOT_TOKEN - токен бота
# - ADMIN_IDS - список администраторов
# - DATABASE_PATH - путь к БД
# - LOG_LEVEL - уровень логирования
# - LANGUAGES - поддерживаемые языки
# - EMOJI_PREMIUM - красивые emoji
```

#### database.py (7.0 KB)
```python
# Работа с БД
# Класс Database с методами:
# - init() - инициализация БД
# - add_user() - добавить пользователя
# - get_user() - получить пользователя
# - set_language() - установить язык
# - add_translation() - добавить перевод
# - get_stats() - получить статистику
# - ban_user() / unban_user() - управление баном
# - get_spam_count() - проверка спама
```

#### translator.py (1.8 KB)
```python
# Логика перевода
# Класс Translator с методами:
# - translate() - перевести текст
# - get_language_code() - получить код языка
# - get_language_name() - получить название языка
```

#### keyboards.py (2.0 KB)
```python
# UI клавиатуры
# Функции:
# - get_language_keyboard() - выбор языка
# - get_main_keyboard() - главное меню
# - get_admin_keyboard() - админ панель
# - get_confirm_keyboard() - подтверждение
```

#### states.py (461 B)
```python
# FSM состояния
# Классы:
# - TranslateStates - состояния перевода
# - AdminStates - состояния админ панели
```

#### handlers.py (14 KB)
```python
# Обработчики команд
# Функции:
# - cmd_start() - команда /start
# - cmd_help() - команда /help
# - cmd_admin() - команда /admin
# - handle_text() - обработка текста
# - handle_language_selection() - выбор языка
# - admin_stats() - статистика
# - admin_broadcast_*() - рассылка
# - admin_ban_*() / admin_unban_*() - управление баном
```

### Конфигурационные файлы

#### requirements.txt (98 B)
```
aiogram==3.3.0
python-dotenv==1.0.0
aiohttp==3.9.1
deep-translator==1.11.4
aiosqlite==0.19.0
```

#### .env (105 B)
```
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_IDS=123456789,987654321
DATABASE_PATH=data/bot.db
LOG_LEVEL=INFO
```

#### .env.example (105 B)
Пример файла .env для новых пользователей

### Документация

#### README.md (7.1 KB)
- Описание проекта
- Поддерживаемые языки
- Основные функции
- Инструкция установки
- Структура проекта
- Команды бота
- Админ функции
- Конфигурация
- БД схема
- Безопасность
- Логирование

#### SETUP.md (3.5 KB)
- Получение токена
- Подготовка окружения
- Конфигурация
- Запуск бота
- Тестирование
- Решение проблем

#### EXAMPLES.md (7.8 KB)
- Пример 1: Простой перевод
- Пример 2: Длинный текст
- Пример 3: Админ команды
- Пример 4: Обработка ошибок
- Пример 5: Выбор языка
- Пример 6: Справка
- Пример 7: Поддерживаемые языки
- Пример 8: Логирование
- Пример 9: Работа с БД
- Пример 10: Безопасность

#### API.md (12 KB)
- Модули и функции
- Класс Database
- Класс Translator
- Функции keyboards
- Состояния FSM
- Обработчики
- Структура данных
- Обработка ошибок
- Логирование
- Асинхронное программирование
- Примеры интеграции

#### DEPLOYMENT.md (13 KB)
- Локальное развертывание
- Развертывание на VPS
- Развертывание с Docker
- Развертывание на Heroku
- Мониторинг и логирование
- Резервное копирование
- Обновление бота
- Решение проблем
- Безопасность
- Масштабирование

#### PROJECT_INFO.md (12 KB)
- Обзор проекта
- Статистика
- Структура
- Технологический стек
- Ключевые особенности
- Документация
- Быстрый старт
- Архитектура
- Безопасность
- Масштабируемость
- Тестирование
- Логирование
- История версий
- Планы на будущее

#### FAQ.md (13 KB)
- Установка и запуск
- Функциональность
- Пользователи
- Безопасность и администрирование
- База данных
- Конфигурация
- Развертывание
- Решение проблем
- Документация
- Советы и трюки
- Поддержка

#### STRUCTURE.md (этот файл)
- Полная структура файлов
- Описание каждого файла
- Размеры файлов
- Зависимости между файлами

## Размеры файлов

| Файл | Размер | Тип |
|------|--------|-----|
| main.py | 1.9 KB | Python |
| config.py | 1.1 KB | Python |
| database.py | 7.0 KB | Python |
| translator.py | 1.8 KB | Python |
| keyboards.py | 2.0 KB | Python |
| states.py | 461 B | Python |
| handlers.py | 14 KB | Python |
| requirements.txt | 98 B | Text |
| .env | 105 B | Text |
| .env.example | 105 B | Text |
| README.md | 7.1 KB | Markdown |
| SETUP.md | 3.5 KB | Markdown |
| EXAMPLES.md | 7.8 KB | Markdown |
| API.md | 12 KB | Markdown |
| DEPLOYMENT.md | 13 KB | Markdown |
| PROJECT_INFO.md | 12 KB | Markdown |
| FAQ.md | 13 KB | Markdown |
| STRUCTURE.md | этот файл | Markdown |
| **ИТОГО** | **~100 KB** | |

## Зависимости между файлами

```
main.py
├── config.py
├── database.py
│   └── config.py
├── handlers.py
│   ├── config.py
│   ├── database.py
│   ├── translator.py
│   ├── keyboards.py
│   └── states.py
└── logging

handlers.py
├── aiogram
├── config.py
├── database.py
├── translator.py
├── keyboards.py
└── states.py

translator.py
├── deep_translator
└── config.py

keyboards.py
├── aiogram
└── config.py

states.py
└── aiogram

database.py
├── aiosqlite
└── config.py
```

## Порядок инициализации

```
1. main.py запускается
   ↓
2. Загружаются переменные окружения (.env)
   ↓
3. Инициализируется config.py
   ↓
4. Инициализируется database.py
   ↓
5. Создается Bot и Dispatcher
   ↓
6. Подключаются handlers.py
   ↓
7. Запускается polling
   ↓
8. Бот готов к работе
```

## Поток данных

```
Пользователь отправляет сообщение
   ↓
handlers.py получает сообщение
   ↓
Проверка состояния (states.py)
   ↓
Обработка текста
   ↓
translator.py переводит текст
   ↓
database.py сохраняет результат
   ↓
keyboards.py показывает кнопки
   ↓
Ответ отправляется пользователю
```

## Как добавить новый файл

1. Создайте новый файл в директории TranslateX
2. Добавьте импорты в main.py если нужно
3. Обновите документацию
4. Протестируйте изменения

## Как удалить файл

1. Удалите файл
2. Удалите импорты из других файлов
3. Обновите документацию
4. Протестируйте изменения

## Лучшие практики

1. **Не редактируйте .env** - используйте .env.example как шаблон
2. **Не коммитьте .env** - добавьте в .gitignore
3. **Не коммитьте __pycache__** - добавьте в .gitignore
4. **Не коммитьте data/bot.db** - это пользовательские данные
5. **Комментируйте код** - используйте русский язык
6. **Следуйте PEP 8** - стиль кода Python
7. **Используйте async/await** - асинхронное программирование
8. **Логируйте действия** - используйте logging модуль

## Расширение проекта

### Добавление нового языка
1. Отредактируйте config.py
2. Добавьте emoji и код языка в LANGUAGES
3. Добавьте название в LANGUAGE_NAMES

### Добавление новой команды
1. Добавьте обработчик в handlers.py
2. Добавьте состояние в states.py если нужно
3. Добавьте кнопку в keyboards.py если нужно

### Добавление новой функции
1. Добавьте метод в Database если нужна работа с БД
2. Добавьте обработчик в handlers.py
3. Добавьте состояние в states.py если нужно
4. Протестируйте функцию

---

**Структура проекта полностью документирована!** ✨

Используйте этот файл как справочник при работе с проектом.
