from django.test import TestCase

from apps.core.mixins import SoftDeleteMixin
from apps.core.models import BaseModel


# 測試用具體模型（結合 SoftDeleteMixin 和 BaseModel）
class SoftDeleteTestModel(SoftDeleteMixin, BaseModel):
    """軟刪除測試用模型"""

    class Meta:
        app_label = "core"


class SoftDeleteMixinTestCase(TestCase):
    """測試 SoftDeleteMixin"""

    def test_soft_delete(self):
        """測試軟刪除：物件仍存在，但 is_active 變為 False"""
        obj = SoftDeleteTestModel.objects.create()
        original_id = obj.id

        # 執行刪除
        obj.delete()

        # 驗證物件仍存在於資料庫
        self.assertTrue(SoftDeleteTestModel.objects.filter(id=original_id).exists())

        # 驗證 is_active 被改為 False
        obj.refresh_from_db()
        self.assertFalse(obj.is_active)

    def test_hard_delete(self):
        """測試真實刪除：物件從資料庫完全消失"""
        obj = SoftDeleteTestModel.objects.create()
        original_id = obj.id

        # TODO: 執行真實刪除（使用 hard_delete()）
        obj.hard_delete()

        # TODO: 驗證物件已經不存在於資料庫（使用 .exists() 驗證為 False）
        self.assertFalse(SoftDeleteTestModel.objects.filter(id=original_id).exists())
