from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

# 匯入我們寫好的工具
from .generators import UserGenerator, PostGenerator, ProductGenerator, CommentGenerator
from .serializers import (
    MockUserSerializer, MockPostSerializer, 
    MockProductSerializer, MockCommentSerializer
)
from apps.core.pagination import StandardResultSetPagination

class BaseMockView(APIView):
    """
    Mock 資料視圖基底類別
    處理共用的參數解析邏輯
    """
    generator_class = None
    serializer_class = None
    pagination_class = StandardResultSetPagination

    def get_params(self, request):
        """解析共用參數"""
        count = request.query_params.get('count', 10)
        locale = request.query_params.get('locale', 'zh_TW')
        
        # 確保 count 是整數且在合理範圍
        try:
            count = min(int(count), 100)  # 最大限制 100 筆，避免效能問題
        except (ValueError, TypeError):
            count = 10
            
        return count, locale

    def get(self, request, *args, **kwargs):
        """處理 GET 請求，加入 Redis 快取機制"""
        count, locale = self.get_params(request)
        
        # 建立專屬的 Cache Key (用生成器名稱 + 數量 + 語系 組成)
        # 例如: mock_PostGenerator_5_zh_TW
        cache_key = f"mock_{self.generator_class.__name__}_{count}_{locale}"
        
        # 1. 嘗試從 Redis 讀取
        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"[Redis Hit] 從快取讀取: {cache_key}")
            return Response(cached_data, status=status.HTTP_200_OK)
            
        print(f"[Redis Miss] 建立新資料: {cache_key}")
        # 2. 如果沒有快取，才產生新資料
        generator = self.generator_class(locale=locale)
        data = generator.generate_multi(count=count)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, request, view=self)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            # 取得 Response 物件後，抽出裡面的 .data (字典格式才能存入 Redis)
            response_data = paginator.get_paginated_response(serializer.data).data
        else:
            serializer = self.serializer_class(data, many=True)
            response_data = serializer.data
            
        # 3. 將最終資料寫入 Redis，設定 60 秒後過期
        cache.set(cache_key, response_data, timeout=60)
        
        return Response(response_data, status=status.HTTP_200_OK)



# --- 具體的 API 視圖 ---

class MockUserListView(BaseMockView):
    """使用者 Mock 資料 API"""
    generator_class = UserGenerator
    serializer_class = MockUserSerializer

class MockPostListView(BaseMockView):
    """文章 Mock 資料 API"""
    generator_class = PostGenerator
    serializer_class = MockPostSerializer

class MockCommentListView(BaseMockView):
    """評論 Mock 資料 API"""
    generator_class = CommentGenerator
    serializer_class = MockCommentSerializer

class MockProductListView(BaseMockView):
    """商品 Mock 資料 API"""
    generator_class = ProductGenerator
    serializer_class = MockProductSerializer