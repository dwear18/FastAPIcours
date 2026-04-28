from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.routers import categories, products, users, reviews, cart, orders


app = FastAPI(
    title="FastAPI Интернет-магазин",
    version="0.1.0",
)


# Сжатие ответов GZip
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Принудительное перенаправление на HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Список разрешённых хостов (укажите свои домены и локальные адреса)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "localhost:3000",
        "127.0.0.1:3000",
        "yourdomain.com",         # ваш боевой домен
        "*.yourdomain.com",       # все поддомены
    ]
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    'null',  # Для тестирования в браузере
    # Добавьте сюда адреса фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(cart.router)
app.include_router(orders.router)

app.mount("/media", StaticFiles(directory="media"), name="media")