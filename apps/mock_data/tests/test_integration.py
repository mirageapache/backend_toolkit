from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache
from apps.mock_data.models import CustomSchema
import uuid


class CustomSchemaIntegrationTest(APITestCase):
    """
    整合測試：模擬使用者從建立模板 -> 用模板生成假資料 -> 刪除模板的完整流程
    """

    def setUp(self):
        cache.clear()

    def test_full_schema_lifecycle(self):
        """
        測試 CustomSchema 的完整生命週期
        步驟：建立 -> 查詢 -> 使用 -> 刪除 -> 確認消失
        """
        # --- Step 1: 建立模板 ---
        create_url = reverse('mock_data:schema-list')
        payload = {
            "name": "整合測試模板",
            "description": "這是一個整合測試用的模板",
            "schema": {
                "user_id": "uuid4",
                "full_name": "name",
                "email": "email",
            }
        }
        create_response = self.client.post(create_url, payload, format='json')

        # 驗證：建立成功，HTTP 201
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        schema_id = create_response.data['id']

        # --- Step 2: 查詢剛建立的模板 ---
        detail_url = reverse('mock_data:schema-detail', kwargs={'pk': schema_id})
        detail_response = self.client.get(detail_url)

        # 驗證：查詢成功
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['name'], '整合測試模板')

        # --- Step 3: 使用此模板生成假資料 ---
        generate_url = reverse('mock_data:custom-mock-data', kwargs={'schema_id': schema_id})
        generate_response = self.client.get(generate_url, {'count': 3})

        # 驗證：生成成功，且資料結構正確
        self.assertEqual(generate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(generate_response.data['count'], 3)
        first_result = generate_response.data['results'][0]
        # 驗證生成的欄位名稱和我們定義的一樣
        self.assertIn('user_id', first_result)
        self.assertIn('full_name', first_result)
        self.assertIn('email', first_result)

        # --- Step 4: 刪除模板 ---
        delete_response = self.client.delete(detail_url)

        # 驗證：刪除成功，HTTP 204 No Content
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # --- Step 5: 確認模板已消失 ---
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_schema_id_returns_404(self):
        """
        測試使用一個不存在的 schema_id 生成資料，應該得到 404
        """
        # TODO: 請完成這個測試案例！
        # 提示 1: 你需要自己捏造一個假的 UUID（Python 的 uuid 套件）
        fake_uuid = uuid.uuid4()
        # 提示 2: 用 reverse 取得 'mock_data:custom-mock-data' 的 URL
        generate_url = reverse('mock_data:custom-mock-data', kwargs={'schema_id': fake_uuid})
        # 提示 3: 發送 GET 請求並驗證 HTTP 404
        generate_response = self.client.get(generate_url)
        self.assertEqual(generate_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_custom_data_with_inline_schema(self):
        """
        測試使用 POST 請求直接傳入 schema 生成資料 (不需存入資料庫)
        """
        url = reverse('mock_data:custom-mock-data-post')
        inline_schema = {
            "product_name": "word",
            "price": "pyint",
        }
        response = self.client.post(url, inline_schema, format='json')

        # 驗證
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 提示：第一筆資料 (results[0]) 應該包含 'product_name' 與 'price' 這兩個 key
        self.assertIn('product_name', response.data['results'][0])
        self.assertIn('price', response.data['results'][0])

    def test_invalid_schema_validation(self):
        """測試當傳入不合法的 Faker 規則時，Serializer 會擋下並回傳 400"""
        create_url = reverse('mock_data:schema-list')
        payload = {
            "name": "惡意測試模板",
            "schema": {
                "valid_field": "uuid4",
                "hacker_field": "os.system('rm -rf')",  # 這個方法 Faker 絕對沒有
                "wrong_type": 123  # 值必須要是字串才對
            }
        }
        create_response = self.client.post(create_url, payload, format='json')

        # 驗證：建立失敗，回傳 HTTP 400 Bad Request
        self.assertEqual(create_response.status_code, status.HTTP_400_BAD_REQUEST)
        # 驗證：錯誤訊息有沒有準確指出出現在 schema 欄位 (注意：我們有自訂 exception_handler！)
        self.assertIn('schema', create_response.data['error']['details'])
