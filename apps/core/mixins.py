from django.utils import timezone


class SoftDeleteMixin:
    """
    軟刪除 Mixin
    提供軟刪除功能，不真正從資料庫刪除資料
    """

    def delete(self, using=None, keep_parents=False):
        """覆寫 delete 方法，改為標記為已刪除"""
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """真正刪除資料"""
        super().delete()


class TimestampMixin:
    """
    時間戳記 Mixin
    自動記錄建立和更新時間
    """

    def save(self, *args, **kwargs):
        if not self.pk:  # 新建立的物件
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
