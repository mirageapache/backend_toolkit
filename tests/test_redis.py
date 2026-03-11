#!/usr/bin/env python
"""
Redis 連線測試腳本
用於驗證 Django 與 Redis 的連接是否正常
"""
import os
import sys

import django

# 設定 Django 環境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from django.conf import settings  # noqa: E402
from django.core.cache import cache  # noqa: E402


def test_redis_connection():
    """測試 Redis 基本連線"""
    print("=" * 60)
    print("Redis 連線測試開始")
    print("=" * 60)

    # 1. 顯示 Redis 配置
    print("\n[1] Redis 配置資訊:")
    redis_config = settings.CACHES.get("default", {})
    print(f"   Backend: {redis_config.get('BACKEND', 'N/A')}")
    print(f"   Location: {redis_config.get('LOCATION', 'N/A')}")

    # 2. 測試寫入
    print("\n[2] 測試寫入快取...")
    test_key = "test_redis_key"
    test_value = "Hello from Django + Redis!"

    try:
        cache.set(test_key, test_value, timeout=60)
        print(f"   ✓ 成功寫入: {test_key} = {test_value}")
    except Exception as e:
        print(f"   ✗ 寫入失敗: {e}")
        return False

    # 3. 測試讀取
    print("\n[3] 測試讀取快取...")
    try:
        retrieved_value = cache.get(test_key)
        if retrieved_value == test_value:
            print(f"   ✓ 成功讀取: {test_key} = {retrieved_value}")
        else:
            print(f"   ✗ 讀取值不符: 期望 '{test_value}', 實際 '{retrieved_value}'")
            return False
    except Exception as e:
        print(f"   ✗ 讀取失敗: {e}")
        return False

    # 4. 測試刪除
    print("\n[4] 測試刪除快取...")
    try:
        cache.delete(test_key)
        deleted_check = cache.get(test_key)
        if deleted_check is None:
            print(f"   ✓ 成功刪除: {test_key}")
        else:
            print("   ✗ 刪除失敗: 鍵值仍存在")
            return False
    except Exception as e:
        print(f"   ✗ 刪除失敗: {e}")
        return False

    # 5. 測試複雜資料結構
    print("\n[5] 測試複雜資料結構...")
    complex_data = {
        "user": "test_user",
        "items": [1, 2, 3, 4, 5],
        "metadata": {"created": "2026-02-11", "active": True},
    }

    try:
        cache.set("complex_test", complex_data, timeout=60)
        retrieved_complex = cache.get("complex_test")
        if retrieved_complex == complex_data:
            print("   ✓ 成功處理複雜資料結構")
        else:
            print("   ✗ 複雜資料不符")
            return False
        cache.delete("complex_test")
    except Exception as e:
        print(f"   ✗ 複雜資料測試失敗: {e}")
        return False

    print("\n" + "=" * 60)
    print("✓ 所有 Redis 測試通過！")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_redis_connection()
    sys.exit(0 if success else 1)
