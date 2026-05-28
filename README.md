# FastAPI E-commerce API

REST API для интернет-магазина, построенный на FastAPI с использованием асинхронной архитектуры.

## Stack

* FastAPI
* SQLAlchemy 2.0
* PostgreSQL
* Alembic
* Docker
* JWT Authentication
* Pydantic v2
* Yookassa
* Loguru

---

# Features

* JWT аутентификация и авторизация
* CRUD для товаров и категорий
* Корзина покупок
* Система заказов
* Отзывы и рейтинги
* PostgreSQL + Alembic migrations
* Docker support
* Логирование приложения

---

# Project Structure

```text
Fastapi_Ecommerce/
├── alembic/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── auth.py
│   ├── schemas.py
│   ├── models/
│   ├── routers/
│   └── services/
├── media/
├── docker-compose.yml
├── pyproject.toml
├── alembic.ini
└── README.md
```

---

# Installation

## 1. Clone repository

```bash
git clone <repository-url>
cd Fastapi_Ecommerce
```

---

## 2. Create virtual environment

```bash
python -m venv venv
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -e .
```

---

# Environment Variables

Create `.env` file in project root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/ecommerce_db

SECRET_KEY=change-this-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

YOOKASSA_SHOP_ID=your-shop-id
YOOKASSA_API_KEY=your-api-key

DEBUG=True
```

---

# Run PostgreSQL with Docker

```bash
docker compose up -d db
```

Check containers:

```bash
docker ps
```

---

# Apply migrations

```bash
alembic upgrade head
```

---

# Run application

```bash
uvicorn app.main:app --reload
```

Application will be available at:

```text
http://localhost:8000
```

---

# API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Main Endpoints

## Authentication

```text
POST   /users/register
POST   /users/login
GET    /users/me
```

## Products

```text
GET    /products
GET    /products/{id}
POST   /products
```

## Categories

```text
GET    /categories
POST   /categories
```

## Cart

```text
GET    /cart
POST   /cart/add
PUT    /cart/{item_id}
DELETE /cart/{item_id}
```

## Orders

```text
POST   /orders
GET    /orders
GET    /orders/{id}
```

## Reviews

```text
POST   /reviews
GET    /reviews/{product_id}
```

---

# Docker Commands

Start all services:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

View logs:

```bash
docker compose logs -f
```

---

# Create New Migration

```bash
alembic revision --autogenerate -m "add new table"
```

Apply migration:

```bash
alembic upgrade head
```

---

# TODO

* Redis caching
* Celery background tasks
* Unit tests
* CI/CD pipeline
* Product image upload
* Admin panel

---

# Notes

* `.env` file is not included in repository
* Use your own PostgreSQL credentials
* For production use secure environment variables and HTTPS

---

# License

MIT
