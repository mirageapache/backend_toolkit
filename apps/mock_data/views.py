from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from django.core.cache import cache

# 匯入我們寫好的工具
from .generators import UserGenerator, PostGenerator, ProductGenerator, CommentGenerator
from .serializers import (
    MockUserSerializer, MockPostSerializer, 
    MockProductSerializer, MockCommentSerializer
)
from apps.core.pagination import StandardResultSetPagination
from .models import CustomSchema
from .serializers import CustomSchemaSerializer
from .generators import CustomGenerator

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

class CustomSchemaViewSet(viewsets.ModelViewSet):
    """
    提供 CustomSchema 的完整 CRUD 功能
    """
    queryset = CustomSchema.objects.filter(is_active=True) # 只查出沒有被軟刪除的資料
    serializer_class = CustomSchemaSerializer
    pagination_class = StandardResultSetPagination

class CustomMockDataView(APIView):
    """
    根據使用者自定義的 Schema 產生假資料 API
    - GET /api/mock/custom/<schema_id>/?count=10 (根據已儲存的模板生成)
    - POST /api/mock/custom/?count=10 (前端直接傳 schema JSON 來即時生成)
    """
    pagination_class = StandardResultSetPagination
    def get(self, request, schema_id=None, *args, **kwargs):
        if not schema_id:
            return Response(
                {"error": "GET 請求必須提供 schema_id，或是如果你想即時生成資料，請改用 POST 請求。"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 取得 count 與 locale 參數
        count = request.query_params.get('count', 10)
        locale = request.query_params.get('locale', 'zh_TW')
        try:
            count = min(int(count), 100)
        except (ValueError, TypeError):
            count = 10

        # 產生 Cache Key (格式：custom_schema_UUID_count_locale)
        cache_key = f"custom_schema_{schema_id}_{count}_{locale}"
        
        # 從 Redis 找
        cached_data = cache.get(cache_key)
        if cached_data:
            print(f"[Redis Hit] 從快取讀取自定義資料: {cache_key}")
            return Response(cached_data, status=status.HTTP_200_OK)

        print(f"[Redis Miss] 建立新的自定義資料: {cache_key}")

        # 如果沒有，先去資料庫撈設定檔
        try:
            schema_obj = CustomSchema.objects.get(id=schema_id, is_active=True)
        except CustomSchema.DoesNotExist:
            raise NotFound("找不到指定的模板")
        # 實例化客製化生成器 (把資料庫裡的 schema 字典丟給它)
        generator = CustomGenerator(
            schema_definition=schema_obj.schema, 
            locale=locale
        )
        # 生成資料
        data = generator.generate_multi(count=count)
        # 分頁處理
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, request, view=self)

        # 抽出最終回傳的字典資料
        if page is not None:
             response_data = paginator.get_paginated_response(page).data
        else:
             response_data = data
             
        # 寫入 Redis
        cache.set(cache_key, response_data, timeout=60)
            
        return Response(response_data, status=status.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):
        """處理前端直接傳遞 JSON schema 來即時生成資料的請求"""
        count = request.query_params.get('count', 10)
        locale = request.query_params.get('locale', 'zh_TW')
        try:
            count = min(int(count), 100)
        except (ValueError, TypeError):
            count = 10
        # 直接從 Request Body 讀取前端傳來的 JSON 規則
        # 例如 frontend 傳來 { "my_id": "uuid4", "score": "pyint" }
        schema_definition = request.data
        
        if not schema_definition or not isinstance(schema_definition, dict):
             return Response(
                 {"error": "請在 Request Body 提供有效的 JSON 格式 Schema 定義"}, 
                 status=status.HTTP_400_BAD_REQUEST
             )
        # 直接把拿到的規則餵給生成器
        generator = CustomGenerator(
            schema_definition=schema_definition, 
            locale=locale
        )
        data = generator.generate_multi(count=count)
        # 處理分頁
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, request, view=self)
        if page is not None:
            return paginator.get_paginated_response(page)
            
        return Response(data, status=status.HTTP_200_OK)