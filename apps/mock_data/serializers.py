from rest_framework import serializers

class MockUserSerializer(serializers.Serializer):
  """使用者資料序列化器"""
  id = serializers.UUIDField()
  name = serializers.CharField(max_length=100)
  email = serializers.EmailField()
  phone = serializers.CharField(max_length=50)
  address = serializers.CharField(max_length=255)
  created_at = serializers.DateTimeField()
    
class MockPostSerializer(serializers.Serializer):
  """文章資料序列化器"""
  id = serializers.UUIDField()
  title = serializers.CharField(max_length=100)
  content = serializers.CharField()
  author_id = serializers.UUIDField()
  created_at = serializers.DateTimeField()
    
class MockCommentSerializer(serializers.Serializer):
  """評論資料序列化器"""
  id = serializers.UUIDField()
  content = serializers.CharField()
  post_id = serializers.UUIDField()
  author_id = serializers.UUIDField()
  created_at = serializers.DateTimeField()
    
class MockProductSerializer(serializers.Serializer):
  """商品資料序列化器"""
  id = serializers.UUIDField()
  name = serializers.CharField(max_length=100)
  price = serializers.IntegerField()
  description = serializers.CharField()
  created_at = serializers.DateTimeField()