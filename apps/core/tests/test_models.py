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

  def test_created_at_auto_set(self):
    """測試 created_at 是否自動設定"""
    obj = TestModel.objects.create()
    
    # 驗證 created_at 已設定
    self.assertIsNotNone(obj.created_at)
    # 驗證時間接近現在（容許 1 秒誤差）
    time_diff = timezone.now() - obj.created_at
    self.assertLess(time_diff.total_seconds(), 1)

  def test_is_active_default_true(self):
      """測試 is_active 預設值為 True"""
      obj = TestModel.objects.create()
      self.assertTrue(obj.is_active)

  def test_updated_at_auto_update(self):
      """測試 updated_at 是否在儲存時自動更新"""
      import time
      obj = TestModel.objects.create()
      original_updated_at = obj.updated_at
      
      time.sleep(0.1)      # 等一下讓時間戳記有所不同
      obj.save()
      obj.refresh_from_db()  # 從資料庫重新讀取最新的值
      
      self.assertGreater(obj.updated_at, original_updated_at)

  def test_ordering_by_created_at(self):
      """測試預設排序為 created_at 降序"""
      import time
      obj1 = TestModel.objects.create()
      time.sleep(0.5)      # 確保兩個物件的時間戳記不同
      obj2 = TestModel.objects.create()
      
      objects = list(TestModel.objects.all())
      
      # 最新的在前面（降序）
      self.assertEqual(objects[0].id, obj2.id)
      self.assertEqual(objects[1].id, obj1.id)
