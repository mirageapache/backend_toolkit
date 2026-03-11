from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MockDataAPITestCase(APITestCase):

    def setUp(self):
        # 每次測試前清空快取，避免測試互相干擾
        cache.clear()

    # --- 1. 使用者 API 測試 ---
    def test_get_mock_users_default(self):
        """測試取得使用者列表 (預設 10 筆)"""
        # 注意: url 反查名稱是在 mock_data/urls.py 定義的 'name'
        url = reverse("mock_data:user-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 驗證預設數量
        self.assertEqual(response.data["count"], 10)
        # 驗證我們自訂的分頁結構
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIn("total_pages", response.data)

    def test_get_mock_users_with_count(self):
        """測試自訂數量的使用者列表 (?count=5)"""
        url = reverse("mock_data:user-list")
        response = self.client.get(url, {"count": 5})  # 加上 query 參數

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        # 確保 results 陣列的長度也是 5
        self.assertEqual(len(response.data["results"]), 5)

    def test_mock_cache_mechanism(self):
        """測試 Redis 快取機制是否運作"""
        url = reverse("mock_data:user-list")

        # 第一次請求 (Miss)
        response1 = self.client.get(url, {"count": 3})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # 驗證資料真的有寫進去 Redis 裡
        # 我們的 Key 設計是: mock_UserGenerator_3_zh_TW
        cached_data = cache.get("mock_UserGenerator_3_zh_TW")
        self.assertIsNotNone(cached_data)

        # 第二次請求 (Hit)
        response2 = self.client.get(url, {"count": 3})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # 驗證兩次拿到的資料是完全一模一樣的 (因為是同一份快取)
        self.assertEqual(response1.data["results"], response2.data["results"])

    # TODO: 2. 文章 API 測試 (post-list)
    def test_get_mock_posts_default(self):
        url = reverse("mock_data:post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIn("total_pages", response.data)

    def test_get_mock_posts_count(self):
        url = reverse("mock_data:post-list")
        response = self.client.get(url, {"count": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(len(response.data["results"]), 5)

    def test_mock_posts_cache_mechanism(self):
        url = reverse("mock_data:post-list")
        response1 = self.client.get(url, {"count": 3})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        cached_data = cache.get("mock_PostGenerator_3_zh_TW")
        self.assertIsNotNone(cached_data)
        response2 = self.client.get(url, {"count": 3})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data["results"], response2.data["results"])

    # TODO: 3. 商品 API 測試 (product-list)
    def test_get_mock_products_default(self):
        url = reverse("mock_data:product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIn("total_pages", response.data)

    def test_get_mock_products_count(self):
        url = reverse("mock_data:product-list")
        response = self.client.get(url, {"count": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(len(response.data["results"]), 5)

    def test_mock_products_cache_mechanism(self):
        url = reverse("mock_data:product-list")
        response1 = self.client.get(url, {"count": 3})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        cached_data = cache.get("mock_ProductGenerator_3_zh_TW")
        self.assertIsNotNone(cached_data)
        response2 = self.client.get(url, {"count": 3})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data["results"], response2.data["results"])

    # TODO: 4. 評論 API 測試 (comment-list)
    def test_get_mock_comments_default(self):
        url = reverse("mock_data:comment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIn("total_pages", response.data)

    def test_get_mock_comments_count(self):
        url = reverse("mock_data:comment-list")
        response = self.client.get(url, {"count": 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)
        self.assertEqual(len(response.data["results"]), 5)

    def test_mock_comments_cache_mechanism(self):
        url = reverse("mock_data:comment-list")
        response1 = self.client.get(url, {"count": 3})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        cached_data = cache.get("mock_CommentGenerator_3_zh_TW")
        self.assertIsNotNone(cached_data)
        response2 = self.client.get(url, {"count": 3})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data["results"], response2.data["results"])
