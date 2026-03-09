from django.db import models
from apps.core.models import BaseModel

# Phase 2 的假資料是即時生成的，不需要存進資料庫
# 這個檔案留給 Phase 3 的 CustomSchema 使用

# 未來 Phase 3 會加入：
# class CustomSchema(BaseModel):
#     name = models.CharField(max_length=100)
#     schema = models.JSONField()
