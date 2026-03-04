from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request           # 重要！DRF 的 Request
from apps.core.pagination import StandardResultSetPagination
from apps.core.models import BaseModel


# 測試用具體模型
class PaginationTestModel(BaseModel):
    class Meta:
        app_label = 'core'
        ordering = ['-created_at']


class PaginationTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.pagination = StandardResultSetPagination()
        
        # 建立 25 筆測試資料
        for i in range(25):
            PaginationTestModel.objects.create()

    def test_default_page_size(self):
        """測試預設每頁 10 筆"""
        # 重點：APIRequestFactory 的 request 需要包裝成 DRF 的 Request 物件
        django_request = self.factory.get('/test/')
        request = Request(django_request)
        
        queryset = PaginationTestModel.objects.all()
        paginated = self.pagination.paginate_queryset(queryset, request)
        self.assertEqual(len(paginated), 10)

    def test_custom_page_size(self):
        """測試自訂每頁筆數（?size=5）"""
        # TODO: 建立帶有 ?size=5 參數的請求
        # TODO: 包裝成 DRF Request
        django_request = self.factory.get('/test/?size=5')
        request = Request(django_request)

        # TODO: 驗證分頁後結果為 5 筆
        queryset = PaginationTestModel.objects.all()
        paginated = self.pagination.paginate_queryset(queryset, request)
        self.assertEqual(len(paginated), 5)

    def test_pagination_response_format(self):
        """測試分頁回應的 JSON 格式"""
        # TODO: 建立請求並執行分頁
        request = self.factory.get('/test/')
        request = Request(request)
        queryset = PaginationTestModel.objects.all()
        paginated = self.pagination.paginate_queryset(queryset, request)
        
        # TODO: 呼叫 get_paginated_response([]) 取得回應
        # TODO: 驗證回應中包含 'links', 'count', 'total_pages', 'current_page', 'results'
        response = self.pagination.get_paginated_response(paginated)
        self.assertIn('links', response.data)
        self.assertIn('count', response.data)
        self.assertIn('total_pages', response.data)
        self.assertIn('current_page', response.data)
        self.assertIn('results', response.data)

