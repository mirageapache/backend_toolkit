from django.urls import path
from . import views

app_name = 'mock_data'

urlpatterns = [
    path('users/', views.MockUserListView.as_view(), name='user-list'),
    path('posts/', views.MockPostListView.as_view(), name='post-list'),
    path('products/', views.MockProductListView.as_view(), name='product-list'),
    path('comments/', views.MockCommentListView.as_view(), name='comment-list'),
]
