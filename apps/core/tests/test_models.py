from django.test import TestCase
from django.utils import timezone
from apps.core.models import BaseModel
import uuid

# 建立測試用的具體模型
class TestModel(BaseModel):
  """測試用模型，繼承 BaseModel"""
  class Meta:
    app_label = 'core'
    ordering = ['-created_at']

class BaseModelTestCase(TestCase):
  """測試 BaseModel 抽象模型"""

  def test_uuid_primary_key(self):
    """測試 UUID 主鍵是否自動生成"""
    # 1.建立一個測試物件
    obj = TestModel.objects.create()
    # 2.驗證 ID 是 UUID 類型
    self.assertIsInstance(obj.id, uuid.UUID)
    # 3.驗證 ID 不是空值
    self.assertIsNotNone(obj.id)