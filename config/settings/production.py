from .base import *

DEBUG = False

ALLOWED_HOSTS = ["your-domain.com"]

# 生產環境通常會透過環境變數讀取資料庫資訊
# import dj_database_url
# DATABASES['default'] = dj_database_url.config()

# 安全性設定
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
