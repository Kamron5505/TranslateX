# 🚀 Инструкция по развертыванию TranslateX

## 📋 Содержание

1. [Локальное развертывание](#локальное-развертывание)
2. [Развертывание на VPS](#развертывание-на-vps)
3. [Развертывание с Docker](#развертывание-с-docker)
4. [Развертывание на Heroku](#развертывание-на-heroku)
5. [Мониторинг и логирование](#мониторинг-и-логирование)

---

## Локальное развертывание

### Windows

#### Шаг 1: Установка Python
```bash
# Скачайте Python 3.8+ с https://www.python.org/
# Убедитесь, что добавили Python в PATH
python --version
```

#### Шаг 2: Клонирование проекта
```bash
git clone https://github.com/yourusername/TranslateX.git
cd TranslateX
```

#### Шаг 3: Создание виртуального окружения
```bash
python -m venv venv
venv\Scripts\activate
```

#### Шаг 4: Установка зависимостей
```bash
pip install -r requirements.txt
```

#### Шаг 5: Конфигурация
```bash
copy .env.example .env
# Отредактируйте .env в текстовом редакторе
```

#### Шаг 6: Запуск
```bash
python main.py
```

### Linux/Mac

#### Шаг 1: Установка Python
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.8 python3-pip python3-venv

# Mac
brew install python3
```

#### Шаг 2: Клонирование проекта
```bash
git clone https://github.com/yourusername/TranslateX.git
cd TranslateX
```

#### Шаг 3: Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Шаг 4: Установка зависимостей
```bash
pip install -r requirements.txt
```

#### Шаг 5: Конфигурация
```bash
cp .env.example .env
nano .env  # Отредактируйте файл
```

#### Шаг 6: Запуск
```bash
python main.py
```

---

## Развертывание на VPS

### Рекомендуемые VPS провайдеры
- DigitalOcean
- Linode
- AWS EC2
- Google Cloud
- Azure

### Инструкция для Ubuntu 20.04

#### Шаг 1: Подключение к серверу
```bash
ssh root@your_server_ip
```

#### Шаг 2: Обновление системы
```bash
apt-get update
apt-get upgrade -y
apt-get install -y python3.8 python3-pip python3-venv git
```

#### Шаг 3: Создание пользователя
```bash
useradd -m -s /bin/bash translatex
su - translatex
```

#### Шаг 4: Клонирование проекта
```bash
git clone https://github.com/yourusername/TranslateX.git
cd TranslateX
```

#### Шаг 5: Установка зависимостей
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Шаг 6: Конфигурация
```bash
cp .env.example .env
nano .env  # Установите BOT_TOKEN и ADMIN_IDS
```

#### Шаг 7: Создание systemd сервиса

Создайте файл `/etc/systemd/system/translatex.service`:

```ini
[Unit]
Description=TranslateX Telegram Bot
After=network.target

[Service]
Type=simple
User=translatex
WorkingDirectory=/home/translatex/TranslateX
Environment="PATH=/home/translatex/TranslateX/venv/bin"
ExecStart=/home/translatex/TranslateX/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Шаг 8: Запуск сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable translatex
sudo systemctl start translatex
sudo systemctl status translatex
```

#### Шаг 9: Просмотр логов
```bash
sudo journalctl -u translatex -f
```

---

## Развертывание с Docker

### Создание Dockerfile

Создайте файл `Dockerfile`:

```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создание директории для БД
RUN mkdir -p data

# Запуск бота
CMD ["python", "main.py"]
```

### Создание docker-compose.yml

```yaml
version: '3.8'

services:
  translatex:
    build: .
    container_name: translatex_bot
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - ADMIN_IDS=${ADMIN_IDS}
      - DATABASE_PATH=data/bot.db
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
    restart: always
    networks:
      - translatex_network

networks:
  translatex_network:
    driver: bridge
```

### Запуск с Docker

```bash
# Создание .env файла
cp .env.example .env
nano .env  # Установите переменные

# Запуск контейнера
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка контейнера
docker-compose down
```

---

## Развертывание на Heroku

### Шаг 1: Установка Heroku CLI
```bash
# Windows
choco install heroku-cli

# Mac
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### Шаг 2: Создание Procfile

Создайте файл `Procfile`:

```
worker: python main.py
```

### Шаг 3: Создание runtime.txt

Создайте файл `runtime.txt`:

```
python-3.8.10
```

### Шаг 4: Инициализация Git репозитория
```bash
git init
git add .
git commit -m "Initial commit"
```

### Шаг 5: Создание Heroku приложения
```bash
heroku login
heroku create your-app-name
```

### Шаг 6: Установка переменных окружения
```bash
heroku config:set BOT_TOKEN=your_token
heroku config:set ADMIN_IDS=123456789
```

### Шаг 7: Развертывание
```bash
git push heroku main
```

### Шаг 8: Просмотр логов
```bash
heroku logs --tail
```

---

## Мониторинг и логирование

### Настройка логирования

#### Логирование в файл

Отредактируйте `main.py`:

```python
import logging.handlers

# Добавьте обработчик файла
file_handler = logging.handlers.RotatingFileHandler(
    'logs/bot.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logging.getLogger().addHandler(file_handler)
```

### Мониторинг производительности

#### Использование памяти
```bash
# Linux
ps aux | grep python
free -h

# Windows
tasklist | findstr python
```

#### Размер БД
```bash
# Linux
du -sh data/bot.db

# Windows
dir data\bot.db
```

### Резервное копирование БД

#### Автоматическое резервное копирование

Создайте скрипт `backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="backups"
DB_FILE="data/bot.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/bot_$TIMESTAMP.db

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "bot_*.db" -mtime +30 -delete

echo "Резервная копия создана: $BACKUP_DIR/bot_$TIMESTAMP.db"
```

#### Добавление в cron

```bash
# Резервная копия каждый день в 2:00 AM
0 2 * * * /home/translatex/TranslateX/backup.sh
```

### Мониторинг статуса бота

#### Скрипт проверки здоровья

Создайте `health_check.py`:

```python
import asyncio
from aiogram import Bot
from config import BOT_TOKEN

async def check_bot_health():
    bot = Bot(token=BOT_TOKEN)
    try:
        me = await bot.get_me()
        print(f"✅ Бот активен: {me.username}")
        return True
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    finally:
        await bot.session.close()

if __name__ == "__main__":
    result = asyncio.run(check_bot_health())
    exit(0 if result else 1)
```

#### Добавление в cron

```bash
# Проверка каждые 5 минут
*/5 * * * * /home/translatex/TranslateX/venv/bin/python /home/translatex/TranslateX/health_check.py
```

---

## Обновление бота

### Обновление кода

```bash
# Остановка бота
sudo systemctl stop translatex

# Обновление кода
cd /home/translatex/TranslateX
git pull origin main

# Установка новых зависимостей
source venv/bin/activate
pip install -r requirements.txt

# Запуск бота
sudo systemctl start translatex
```

### Миграция БД

Если вы изменили схему БД, создайте скрипт миграции:

```python
# migrate.py
import asyncio
from database import Database

async def migrate():
    db = Database()
    # Добавьте новые таблицы или колонки
    async with aiosqlite.connect(db.db_path) as database:
        await database.execute("""
            ALTER TABLE users ADD COLUMN new_column TEXT DEFAULT NULL
        """)
        await database.commit()

if __name__ == "__main__":
    asyncio.run(migrate())
```

---

## Решение проблем

### Бот не запускается

```bash
# Проверьте логи
sudo journalctl -u translatex -n 50

# Проверьте конфигурацию
cat /home/translatex/TranslateX/.env

# Проверьте права доступа
ls -la /home/translatex/TranslateX/
```

### Высокое использование памяти

```bash
# Перезагрузите бота
sudo systemctl restart translatex

# Проверьте размер БД
du -sh data/bot.db

# Очистите старые логи
rm -rf logs/*
```

### Ошибки перевода

```bash
# Проверьте интернет соединение
ping google.com

# Проверьте API лимиты
# Используйте VPN если нужно
```

---

## Безопасность при развертывании

### Рекомендации

1. **Используйте переменные окружения** для всех секретов
2. **Ограничьте доступ к серверу** через firewall
3. **Используйте SSH ключи** вместо пароля
4. **Регулярно обновляйте** зависимости
5. **Создавайте резервные копии** БД
6. **Мониторьте логи** на предмет ошибок
7. **Используйте HTTPS** для веб интерфейсов

### Firewall правила

```bash
# Разрешить SSH
sudo ufw allow 22/tcp

# Разрешить HTTP
sudo ufw allow 80/tcp

# Разрешить HTTPS
sudo ufw allow 443/tcp

# Включить firewall
sudo ufw enable
```

---

## Масштабирование

### Для большого количества пользователей

1. **Используйте PostgreSQL** вместо SQLite
2. **Используйте Redis** для кэширования
3. **Используйте Kubernetes** для оркестрации
4. **Используйте Load Balancer** для распределения нагрузки
5. **Используйте CDN** для статических файлов

### Пример с PostgreSQL

```python
# Установка
pip install asyncpg

# Использование
DATABASE_URL = "postgresql://user:password@localhost/translatex"
```

---

**Развертывание готово!** 🚀

Выберите подходящий вариант и следуйте инструкциям.
