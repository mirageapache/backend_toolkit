from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "mock_data"


# 1. 建立 Router 並把我們的 ViewSet 註冊進去
router = DefaultRouter()
# 這會自動生出 /schemas/ 和 /schemas/<id>/ 的路由
router.register(r"schemas", views.CustomSchemaViewSet, basename="schema")
urlpatterns = [
    path("users/", views.MockUserListView.as_view(), name="user-list"),
    path("posts/", views.MockPostListView.as_view(), name="post-list"),
    path("products/", views.MockProductListView.as_view(), name="product-list"),
    path("comments/", views.MockCommentListView.as_view(), name="comment-list"),
    path(
        "custom/<uuid:schema_id>/",
        views.CustomMockDataView.as_view(),
        name="custom-mock-data",
    ),
    path("custom/", views.CustomMockDataView.as_view(), name="custom-mock-data-post"),
    # Router 產生的路由
    path("", include(router.urls)),
]
