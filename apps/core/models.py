import uuid

from django.db import models


class BaseModel(models.Model):
    """
    抽象基礎模型
    提供所有 Model 共用的欄位：ID, 建立時間, 更新時間, 刪除標記
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")

    class Meta:
        abstract = True
        ordering = ["-created_at"]
