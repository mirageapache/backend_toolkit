#!/usr/bin/env python
"""
環境驗證腳本
檢查 Phase 1 的所有基礎設施是否正常運作
"""
import os
import sys
import django

# 設定 Django 環境（因為這是獨立腳本，不走 manage.py，需要手動設定）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.cache import cache
from django.db import connection
from django.conf import settings


def check_database():
    """檢查 PostgreSQL 連線"""
    print("\n[PostgreSQL 資料庫檢查]")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"  ✓ 連線成功: {version.split(',')[0]}")
        return True
    except Exception as e:
        print(f"  ✗ 連線失敗: {e}")
        return False


def check_redis():
    """檢查 Redis 快取"""
    print("\n[Redis 快取檢查]")
    try:
        # TODO: 寫入一個測試 key/value
        # TODO: 讀取並驗證值是否正確
        # TODO: 刪除這個 key
        # TODO: 每步驟印出 ✓ 或 ✗ 的結果
        cache.set('test_key', 'test_value', timeout=10)
        test_key = cache.get('test_key')
        if test_key == 'test_value':
            print("  ✓ 寫入並讀取成功")
            cache.delete('test_key')
            return True
        else:
            print("  ✗ 寫入並讀取失敗")
            cache.delete('test_key')
            return False
    except Exception as e:
        print(f"  ✗ 連線失敗: {e}")
        return False


def check_installed_apps():
    """檢查關鍵 App 是否已安裝"""
    print("\n[已安裝 Apps 檢查]")
    from django.apps import apps
    
    key_apps = ['core', 'rest_framework', 'corsheaders']
    
    # TODO: 逐一檢查 key_apps 中的每個 app
    # 提示：使用 apps.get_app_config(app_name) 取得 app
    #       用 try/except LookupError 處理找不到的情況
    is_installed = True
    for app_name in key_apps:
      try:
        apps.get_app_config(app_name)
        print(f"  ✓ 已安裝: {app_name}")
      except LookupError:
        print(f"  ✗ 未安裝: {app_name}")
        is_installed = False
    return is_installed

def main():
    print("=" * 50)
    print("  Phase 1 環境驗證")
    print("=" * 50)
    
    results = []
    results.append(("PostgreSQL", check_database()))
    results.append(("Redis", check_redis()))
    results.append(("Installed Apps", check_installed_apps()))
    
    print("\n[驗證總結]")
    passed = sum(1 for _, r in results if r)
    for name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"  {status}: {name}")
    
    print(f"\n總計: {passed}/{len(results)} 項通過")
    
    if passed == len(results):
        print("\n🎉 Phase 1 環境配置完成！")
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
