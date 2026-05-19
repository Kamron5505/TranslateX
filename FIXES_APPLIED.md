# Исправления, примененные к проекту TranslateX

## Проблема 1: Команда /start не работала

### Причина
В файле `handlers.py` создавался новый экземпляр `Database()` без инициализации:
```python
db = Database()  # ❌ Не инициализирована
```

Это приводило к ошибкам при попытке использовать методы БД в обработчиках команд.

### Решение
1. **handlers.py**: Изменили инициализацию БД на глобальную переменную с функцией установки:
```python
db = None

def set_db(database):
    """Установить экземпляр БД"""
    global db
    db = database
```

2. **main.py**: Добавили импорт функции `set_db` и вызов её после инициализации БД:
```python
from handlers import router, set_db

# ... в функции main():
await db.init()
set_db(db)  # ✅ Передаем инициализированную БД в handlers
```

## Проблема 2: Railway не может собрать приложение

### Причина
Railway ищет файлы проекта в корне репозитория, но все файлы находятся в подпапке `TranslateX/`.

### Решение
Обновить `railway.json` в корне проекта, добавив параметр `rootDirectory`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "rootDirectory": "TranslateX"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "always",
    "restartPolicyMaxRetries": 5
  }
}
```

## Проблема 3: ValueError при пустом ADMIN_IDS на Railway

### Причина
На Railway переменная окружения `ADMIN_IDS` может быть пуста или не установлена, что приводило к ошибке:
```
ValueError: invalid literal for int() with base 10: ''
```

### Решение
Обновить `config.py` для обработки пустых значений:
```python
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS = list(map(int, ADMIN_IDS_STR.split(","))) if ADMIN_IDS_STR else []
```

Теперь если `ADMIN_IDS` пуста, будет использован пустой список `[]`.

## Тестирование

Все компоненты протестированы локально:

✅ **Импорты** - все модули импортируются без ошибок
✅ **Конфигурация** - BOT_TOKEN установлен, ADMIN_IDS загружены
✅ **Пустой ADMIN_IDS** - корректно обрабатывается как пустой список
✅ **База данных** - инициализируется и работает корректно
✅ **Переводчик** - успешно переводит текст
✅ **Обработчики** - готовы к использованию

## Файлы, которые были изменены

1. `TranslateX/main.py` - добавлен импорт `set_db` и вызов функции
2. `TranslateX/handlers.py` - изменена инициализация БД на глобальную переменную
3. `TranslateX/config.py` - добавлена обработка пустого ADMIN_IDS
4. `railway.json` - добавлен параметр `rootDirectory` (требует ручного обновления)
5. `.env.railway` - обновлена переменная ADMIN_IDS

## Следующие шаги

1. Обновить `railway.json` в корне проекта (см. выше)
2. Убедиться, что на Railway установлены переменные окружения:
   - `BOT_TOKEN` - токен бота
   - `ADMIN_IDS` - ID администраторов (опционально, может быть пусто)
3. Запустить бота локально: `python TranslateX/main.py`
4. Протестировать команду `/start` в Telegram
5. Развернуть на Railway

## Команды для локального тестирования

```bash
# Установить зависимости
pip install -r TranslateX/requirements.txt

# Запустить тесты
python TranslateX/test_simple.py
python TranslateX/test_empty_admin.py

# Запустить бота
python TranslateX/main.py
```
