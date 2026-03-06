from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# 匯入我們寫好的工具
from .generators import UserGenerator, PostGenerator, ProductGenerator, CommentGenerator
from .serializers import (
    MockUserSerializer, MockPostSerializer, 
    MockProductSerializer, MockCommentSerializer
)

class BaseMockView(APIView):
    """
    Mock 資料視圖基底類別
    處理共用的參數解析邏輯
    """
    generator_class = None
    serializer_class = None

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
        """處理 GET 請求"""
        count, locale = self.get_params(request)
        
        # 1. 實例化生成器
        generator = self.generator_class(locale=locale)
        
        # 2. 生成資料 (由子類別提供方法名)
        data = generator.generate_multi(count=count)
        
        # 3. 序列化資料
        serializer = self.serializer_class(data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


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