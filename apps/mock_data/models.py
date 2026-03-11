from django.db import models

from apps.core.models import BaseModel

# Phase 2 的假資料是即時生成的，不需要存進資料庫
# 這個檔案留給 Phase 3 的 CustomSchema 使用


# 未來 Phase 3 會加入：
class CustomSchema(BaseModel):
    """
    使用者自定義的資料生成模板
    繼承自 BaseModel，自動獲得 id, created_at, updated_at, is_active欄位
    """

    name = models.CharField(max_length=100, help_text="模板名稱")
    description = models.TextField(blank=True, help_text="模板說明")
    schema = models.JSONField(help_text="Faker 生成規則定義")

    class Meta:
        db_table = "mock_data_custom_schema"  # 自訂資料表名稱
        verbose_name = "自定義模板"
        verbose_name_plural = "自定義模板"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.id})"
