# FastAPI Интернет-магазин

Полнофункциональное REST API приложение для интернет-магазина, построенное на FastAPI с использованием PostgreSQL базы данных.

## 🎯 Описание проекта

**FastAPI Интернет-магазин** — это современное E-commerce решение с поддержкой:
- Управления товарами и категориями
- Пользовательских аккаунтов с JWT аутентификацией
- Системы корзины покупок
- Оформления заказов
- Обработки платежей через Yookassa
- Системы отзывов и рейтингов
- Логирования всех операций

Приложение использует асинхронную архитектуру для обработки высоконагруженных операций.

## 📋 Требования

- **Python**: 3.12+
- **Docker**: последняя версия
- **Docker Compose**: последняя версия
- **Git**: для клонирования репозитория

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd Fastapi_Ecommerce
```

### 2. Установка зависимостей

```bash
# Создайте виртуальное окружение
python3.12 -m venv venv

# Активируйте виртуальное окружение
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -e .
```

### 3. Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Database
DATABASE_URL=postgresql+asyncpg://ecommerce_user:12345556rR@localhost:5432/ecommerce_db

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Yookassa (платежи)
YOOKASSA_SHOP_ID=your-shop-id
YOOKASSA_API_KEY=your-api-key

# App
DEBUG=True
HOST=localhost
PORT=8000
```

### 4. Запуск PostgreSQL через Docker

```bash
# Запустите контейнер PostgreSQL
docker-compose up -d db

# Проверьте, что база данных запустилась
docker ps
```

**Параметры подключения PostgreSQL:**
- **User**: ecommerce_user
- **Password**: 12345556rR
- **Database**: ecommerce_db
- **Port**: 5432

### 5. Применение миграций базы данных

```bash
# Создайте все необходимые таблицы
alembic upgrade head
```

### 6. Запуск приложения

```bash
# Запустите FastAPI сервер на localhost:8000
uvicorn app.main:app --reload

# Для запуска на определенном хосте и порте
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Приложение будет доступно по адресу: **http://localhost:8000**

## 📚 API документация

После запуска приложения:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📦 Основные зависимости

| Пакет | Версия | Назначение |
|-------|--------|-----------|
| FastAPI | ≥0.135.1 | Web фреймворк |
| Uvicorn | ≥0.41.0 | ASGI сервер |
| SQLAlchemy | ≥2.0.48 | ORM для работы с БД |
| asyncpg | ≥0.31.0 | Драйвер PostgreSQL |
| Alembic | ≥1.18.4 | Миграции БД |
| Pydantic | ≥2.12.5 | Валидация данных |
| PyJWT | ≥2.12.1 | JWT токены |
| bcrypt | 4.0.1 | Хеширование паролей |
| Yookassa | ≥3.10.1 | Платежная система |
| Loguru | ≥0.7.3 | Логирование |
| python-dotenv | ≥1.2.2 | Переменные окружения |

## 📂 Структура проекта

```
Fastapi_Ecommerce/
├── alembic.ini                 # Конфиг Alembic для миграций
├── docker-compose.yml          # Docker Compose конфиг
├── pyproject.toml             # Конфиг проекта и зависимости
├── README.md                  # Этот файл
├── dump.sql                   # Дамп БД
├── app/
│   ├── __init__.py
│   ├── main.py               # Основное приложение FastAPI
│   ├── auth.py               # Логика аутентификации
│   ├── config.py             # Конфигурация приложения
│   ├── database.py           # Подключение к БД
│   ├── db_depends.py         # Зависимости для БД
│   ├── schemas.py            # Pydantic схемы
│   ├── migrations/           # Миграции Alembic
│   ├── models/               # SQLAlchemy модели
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   ├── orders.py
│   │   ├── cart_items.py
│   │   └── reviews.py
│   └── routers/              # API маршруты
│       ├── users.py
│       ├── products.py
│       ├── categories.py
│       ├── orders.py
│       ├── cart.py
│       └── reviews.py
└── media/                    # Медиафайлы
    └── products/             # Изображения товаров
```

## 🔑 Основные компоненты

### 🛡️ Аутентификация

Система использует JWT токены для аутентификации. Пароли хранятся с использованием bcrypt хеширования.

**Примеры эндпоинтов:**
- `POST /users/register` - Регистрация пользователя
- `POST /users/login` - Вход в систему
- `GET /users/me` - Получение информации о текущем пользователе

### 📦 Товары и категории

- `GET /products` - Получить все товары
- `GET /products/{id}` - Получить товар по ID
- `POST /products` - Создать новый товар (только администратор)
- `GET /categories` - Получить все категории
- `POST /categories` - Создать новую категорию (только администратор)

### 🛒 Корзина покупок

- `GET /cart` - Получить содержимое корзины
- `POST /cart/add` - Добавить товар в корзину
- `DELETE /cart/{item_id}` - Удалить товар из корзины
- `PUT /cart/{item_id}` - Обновить количество товара

### 📋 Заказы

- `POST /orders` - Создать новый заказ
- `GET /orders` - Получить мои заказы
- `GET /orders/{id}` - Получить информацию о заказе

### ⭐ Отзывы

- `POST /reviews` - Оставить отзыв о товаре
- `GET /reviews/{product_id}` - Получить отзывы о товаре

## 🔧 Дополнительные команды

### Создание новой миграции

```bash
# После изменения моделей создайте новую миграцию
alembic revision --autogenerate -m "Description of changes"

# Примените миграцию
alembic upgrade head
```

### Просмотр логов

```bash
# Основной лог приложения находится в файле info.log
tail -f info.log
```

### Работа с Docker

```bash
# Запустить все сервисы
docker-compose up -d

# Остановить все сервисы
docker-compose down

# Просмотреть логи
docker-compose logs -f

# Удалить базу данных (осторожно!)
docker-compose down -v
```

## 🧪 Тестирование

```bash
# Проверка синтаксиса Python
python -m py_compile app/*.py app/models/*.py app/routers/*.py

# Запуск линтера (если установлен)
# flake8 app/
```

## 📝 Переменные окружения

Полный список доступных переменных окружения:

| Переменная | Описание | Значение по умолчанию |
|-----------|---------|----------------------|
| `DATABASE_URL` | URL подключения к БД | - |
| `SECRET_KEY` | Секретный ключ для JWT | - |
| `ALGORITHM` | Алгоритм для JWT | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена | 30 |
| `YOOKASSA_SHOP_ID` | ID магазина Yookassa | - |
| `YOOKASSA_API_KEY` | API ключ Yookassa | - |
| `DEBUG` | Режим отладки | False |
| `HOST` | Хост приложения | localhost |
| `PORT` | Порт приложения | 8000 |

## 🐛 Решение проблем

### Ошибка подключения к БД

```
sqlalchemy.exc.OperationalError: (asyncpg.exceptions.CannotConnectNowError)
```

**Решение:** Убедитесь, что PostgreSQL контейнер запущен:
```bash
docker-compose up -d db
docker ps  # Проверьте наличие контейнера
```

### Ошибка миграции БД

```
ERROR: Can't connect to database
```

**Решение:** Проверьте переменную `DATABASE_URL` в `.env` файле и убедитесь, что база данных доступна.

### Порт 8000 уже занят

```bash
# Запустите на другом порту
uvicorn app.main:app --port 8001
```

### Ошибка импорта модулей

```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate

# Переустановите зависимости
pip install -e .
```

## 🔐 Безопасность

⚠️ **Для production:**

1. Измените значение `SECRET_KEY` на надежное
2. Установите `DEBUG = False`
3. Используйте переменные окружения для всех чувствительных данных
4. Настройте CORS для разрешенных доменов
5. Используйте HTTPS
6. Ограничьте количество запросов (Rate Limiting)

## 📞 Поддержка

Если у вас возникнут проблемы:

1. Проверьте логи приложения в `info.log`
2. Убедитесь, что все зависимости установлены
3. Проверьте, что PostgreSQL запущен и доступен
4. Проверьте файл `.env` на корректность переменных

## 📄 Лицензия

MIT License

---

**Версия:** 0.1.0  
**Последнее обновление:** Май 2026
