from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# --- 資料庫設定 (連接 Docker 中的 PostgreSQL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'backend_toolkit',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# --- Redis 設定 ---
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 可以在這裡加入額外的開發工具設定 (例如 django-debug-toolbar)
