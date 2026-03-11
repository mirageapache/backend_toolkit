from rest_framework import serializers
from .models import CustomSchema
from faker import Faker

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

class CustomSchemaSerializer(serializers.ModelSerializer):
    """自定義 Schema 的序列化器"""
    
    class Meta:
        model = CustomSchema
        fields = ['id', 'name', 'description', 'schema', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_schema(self, value):
        """
        針對 schema 欄位進行客製化驗證
        檢查傳入的字典中，每一個 value 是否都是合法的 Faker 方法
        """
        # 1. 確保傳入的是字典 (Dictionary)
        if not isinstance(value, dict):
            raise serializers.ValidationError("Schema 必須是一個 JSON 字典 (Object)。")

        # 2. 準備一個 Faker 實例用來當對照手冊
        fake = Faker()
        
        # 3. 檢查每一個設定的規則
        invalid_methods = []
        for field, method_name in value.items():
            # 必須是字串
            if not isinstance(method_name, str):
                raise serializers.ValidationError(f"欄位 {field} 的規則必須是字串 (Faker 方法名稱)。")
            
            # 拿 method_name 去翻 Faker 的手冊，看有沒有這個方法可以呼叫
            # 例如 method_name 是 'uuid4'，就會去找 fake.uuid4 是否存在
            if not hasattr(fake, method_name) or not callable(getattr(fake, method_name)):
                invalid_methods.append(method_name)

        # 4. 如果有找到不合法的方法，把錯誤一次報給前端
        if invalid_methods:
            # 將 list 變成以逗號分隔的字串
            err_str = ", ".join(invalid_methods)
            raise serializers.ValidationError(f"包含不支援的 Faker 生成規則：{err_str}。請參閱 Faker 官方文件。")
            
        return value

