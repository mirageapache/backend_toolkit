from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
  """
  自定義權限：
    - 僅管理員具有寫入權限
    - 其他使用者僅具有讀取權限
  """
  def has_permission(self, request, view):
    # 安全的方法(GET, HEAD, OPTIONS)允許所有人存取
    if request.method in permissions.SAFE_METHODS:
      return True
    # 寫入方法(POST, PUT, PATCH, DELETE)僅允許管理員存取
    return bool(request.user and request.user.is_staff)