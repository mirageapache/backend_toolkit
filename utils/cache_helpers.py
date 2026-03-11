"""
Redis 快取工具函數
提供常用的快取操作封裝
"""

import hashlib
import json
from functools import wraps

from django.core.cache import cache


def cache_key_generator(*args, **kwargs):
    """
    生成快取鍵值
    根據函數參數自動生成唯一的快取鍵
    """
    key_data = {"args": args, "kwargs": kwargs}
    key_string = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_string.encode()).hexdigest()


def cached(timeout=300, key_prefix=""):
    """
    快取裝飾器

    使用方式:
    @cached(timeout=600, key_prefix='user_data')
    def get_user_data(user_id):
        # 耗時的資料庫查詢
        return expensive_query(user_id)

    Args:
        timeout: 快取過期時間（秒），預設 300 秒
        key_prefix: 快取鍵前綴
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成快取鍵
            cache_key = (
                f"{key_prefix}:{func.__name__}:{cache_key_generator(*args, **kwargs)}"
            )

            # 嘗試從快取取得
            result = cache.get(cache_key)

            if result is not None:
                return result

            # 快取未命中，執行函數
            result = func(*args, **kwargs)

            # 儲存到快取
            cache.set(cache_key, result, timeout=timeout)

            return result

        return wrapper

    return decorator


def invalidate_cache(key_pattern):
    """
    清除符合模式的快取

    Args:
        key_pattern: 快取鍵模式
    """
    cache.delete_pattern(key_pattern)


def get_or_set_cache(key, default_func, timeout=300):
    """
    取得快取，若不存在則執行函數並設定快取

    Args:
        key: 快取鍵
        default_func: 當快取不存在時執行的函數
        timeout: 快取過期時間（秒）

    Returns:
        快取值或函數執行結果
    """
    result = cache.get(key)

    if result is None:
        result = default_func()
        cache.set(key, result, timeout=timeout)

    return result


# 使用範例
if __name__ == "__main__":
    # 範例 1: 使用裝飾器
    @cached(timeout=600, key_prefix="example")
    def expensive_calculation(x, y):
        """模擬耗時計算"""
        import time

        time.sleep(2)  # 模擬耗時操作
        return x + y

    # 第一次呼叫會執行函數（耗時 2 秒）
    result1 = expensive_calculation(10, 20)

    # 第二次呼叫會從快取取得（幾乎瞬間）
    result2 = expensive_calculation(10, 20)

    print(f"Result: {result1}, {result2}")

    # 範例 2: 使用 get_or_set_cache
    def fetch_data():
        return {"data": "expensive query result"}

    data = get_or_set_cache("my_data_key", fetch_data, timeout=300)
    print(f"Data: {data}")
