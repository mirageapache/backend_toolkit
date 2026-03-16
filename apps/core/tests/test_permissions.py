from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from apps.core.permissions import IsAdminOrReadOnly


class IsAdminOrReadOnlyTestCase(TestCase):
    """測試 IsAdminOrReadOnly 權限"""

    def setUp(self):
        """設定測試環境（每個測試方法執行前都會跑一次）"""
        self.factory = APIRequestFactory()
        self.permission = IsAdminOrReadOnly()
        self.view = APIView()

        # 建立一般使用者
        self.normal_user = User.objects.create_user(
            username="user", password="user123", is_staff=False
        )
        # 建立管理員使用者
        self.admin_user = User.objects.create_user(
            username="admin", password="admin123", is_staff=True
        )

    def test_get_allowed_for_anonymous(self):
        """測試 GET 請求對匿名用戶開放"""
        request = self.factory.get("/test/")
        request.user = AnonymousUser()
        result = self.permission.has_permission(request, self.view)
        self.assertTrue(result)

    def test_post_denied_for_normal_user(self):
        """測試 POST 請求對一般用戶拒絕"""
        # TODO: 建立 POST 請求
        request = self.factory.post("/test/")
        # TODO: 設定 request.user 為一般用戶
        request.user = self.normal_user
        # TODO: 驗證 has_permission 回傳 False
        result = self.permission.has_permission(request, self.view)
        self.assertFalse(result)

    def test_post_allowed_for_admin(self):
        """測試 POST 請求對管理員允許"""
        # TODO: 建立 POST 請求
        request = self.factory.post("/test/")
        # TODO: 設定 request.user 為管理員
        request.user = self.admin_user
        # TODO: 驗證 has_permission 回傳 True
        result = self.permission.has_permission(request, self.view)
        self.assertTrue(result)
