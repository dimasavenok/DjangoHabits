# Habits Telegram Bot

Система управления привычками с интеграцией Telegram для отправки напоминаний.

## Возможности

- ✅ Создание и управление привычками
- ✅ Валидация данных согласно бизнес-правилам
- ✅ Интеграция с Telegram для напоминаний
- ✅ Отложенные задачи через Celery
- ✅ REST API с документацией
- ✅ Пагинация и фильтрация
- ✅ Права доступа и аутентификация
- ✅ CORS для фронтенда

## Установка

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте файл `env.example` в `.env` и заполните необходимые переменные:

```bash
cp env.example .env
```

Отредактируйте `.env` файл:

```env
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here

# Redis for Celery
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 3. Создание Telegram бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Получите токен бота и добавьте его в `.env` файл

### 4. Настройка базы данных

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Запуск сервисов

#### Запуск Django сервера:
```bash
python manage.py runserver
```

#### Запуск Celery Worker (в отдельном терминале):
```bash
celery -A config worker --loglevel=info
```

#### Запуск Celery Beat (в отдельном терминале):
```bash
celery -A config beat --loglevel=info
```


## API Endpoints - TODO

### Аутентификация (JWT)
- `POST /api/v1/auth/register/` - Регистрация пользователя
- `POST /api/v1/auth/login/` - Авторизация пользователя
- `POST /api/v1/auth/logout/` - Выход пользователя (blacklist refresh token)
- `POST /api/v1/auth/token/` - Получение JWT токенов
- `POST /api/v1/auth/token/refresh/` - Обновление access token

### Привычки
- `GET /api/v1/habits/` - Список привычек пользователя (с пагинацией)
- `POST /api/v1/habits/` - Создание привычки
- `GET /api/v1/habits/{id}/` - Детали привычки
- `PUT /api/v1/habits/{id}/` - Обновление привычки
- `DELETE /api/v1/habits/{id}/` - Удаление привычки
- `GET /api/v1/habits/public/` - Список публичных привычек

### Telegram
- `GET /api/v1/telegram/user/` - Информация о Telegram пользователе
- `POST /api/v1/telegram/connect/` - Подключение Telegram аккаунта
- `DELETE /api/v1/telegram/disconnect/` - Отключение Telegram аккаунта
- `GET /api/v1/telegram/messages/` - История сообщений

### Документация API
- `GET /swagger/` - Swagger UI
- `GET /redoc/` - ReDoc


### Валидация
1. Нельзя одновременно указывать связанную привычку и вознаграждение
2. Время выполнения не должно превышать 120 секунд
3. Связанные привычки должны быть приятными
4. У приятных привычек не может быть вознаграждения или связанной привычки
5. Периодичность не может быть больше 7 дней

## Права доступа

- Каждый пользователь имеет доступ только к своим привычкам (CRUD)
- Пользователи могут просматривать публичные привычки (только чтение)
- Аутентификация через JWT токены (access + refresh)
- JWT настройки: Access token (60 мин), Refresh token (7 дней)
- Автоматическая ротация refresh токенов
- Blacklist для недействительных токенов

## Telegram интеграция

Бот поддерживает следующие команды:
- `/start` - Начать работу с ботом
- `/habits` - Показать привычки пользователя
- `/connect` - Инструкции по подключению аккаунта

## Celery задачи

- `send_habit_reminders` - Отправка напоминаний о привычках (каждую минуту)

## Разработка

### Структура проекта - TODO
```
habits_telegram/
├── config/                 # Настройки Django
├── habitsapp/             # Приложение для привычек
├── telegramapp/           # Приложение для Telegram
├── mainapp/              # Основное приложение
├── requirements.txt      # Зависимости
├── env.example          # Пример переменных окружения
└── README.md           # Документация
```

### Тестирование
```bash
python manage.py test
```

### Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```


