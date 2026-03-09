from faker import Faker

class BaseGenerator:
  """
  基礎資料生成器
  所有 Generator 的父類別，定義共用介面
  """
  def __init__(self, locale="zh_TW"):
    """
    locale: 語系設定
      - 'zh_TW' 繁體中文
      - 'en_US' 英文
    """
    self.fake = Faker(locale)
    Faker.seed(0) # 固定seed，讓測試結果可重現

  def generate_multi(self, count=10):
    """
    生成指定數量的假資料
    子類別必須實作這個方法
    """
    raise NotImplementedError("子類別必須實作 generate_multi() 方法")

  def generate_one(self):
    """生成單筆假資料"""
    raise NotImplementedError("子類別必須實作 generate_one() 方法")

class UserGenerator(BaseGenerator):
    """使用者資料生成器"""
    
    def generate_one(self):
        """生成單筆使用者資料"""
        return {
            'id': str(self.fake.uuid4()),
            'name': self.fake.name(),
            'email': self.fake.email(),
            'phone': self.fake.phone_number(),
            'address': self.fake.address(),
            'created_at': self.fake.date_time_this_year().isoformat(),
        }
    
    def generate_multi(self, count=10):
        """生成多筆使用者資料"""
        return [self.generate_one() for _ in range(count)]

class PostGenerator(BaseGenerator):
    """文章資料生成器"""
    
    def generate_one(self):
        """生成單筆文章資料"""
        return {
            'id': str(self.fake.uuid4()),
            'title': self.fake.sentence(nb_words=6, variable_nb_words=True),
            'content': self.fake.text(),
            'author_id': str(self.fake.uuid4()),
            'created_at': self.fake.date_time_this_year().isoformat(),
        }

    def generate_multi(self, count=10):
        """生成多筆文章資料"""
        return [self.generate_one() for _ in range(count)]

class CommentGenerator(BaseGenerator):
    """評論資料生成器"""
    
    def generate_one(self):
        """生成單筆評論資料"""
        return {
            'id': str(self.fake.uuid4()),
            'content': self.fake.text(),
            'post_id': str(self.fake.uuid4()),
            'author_id': str(self.fake.uuid4()),
            'created_at': self.fake.date_time_this_year().isoformat(),
        }
    
    def generate_multi(self, count=10):
        """生成多筆評論資料"""
        return [self.generate_one() for _ in range(count)]

class ProductGenerator(BaseGenerator):
    """商品資料生成器"""
    
    def generate_one(self):
        """生成單筆商品資料"""
        return {
            'id': str(self.fake.uuid4()),
            'name': self.fake.word(),
            'price': self.fake.pyint(min_value=100, max_value=5000),
            'description': self.fake.text(),
            'created_at': self.fake.date_time_this_year().isoformat(),
        }
    
    def generate_multi(self, count=10):
        """生成多筆商品資料"""
        return [self.generate_one() for _ in range(count)]
