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
        Faker.seed(0)  # 固定seed，讓測試結果可重現

    def generate_multi(self, count=10):
        """生成指定數量的假資料"""
        return [self.generate_one() for _ in range(count)]

    def generate_one(self):
        """生成單筆假資料"""
        raise NotImplementedError("子類別必須實作 generate_one() 方法")


class UserGenerator(BaseGenerator):
    """使用者資料生成器"""

    def generate_one(self):
        """生成單筆使用者資料"""
        return {
            "id": str(self.fake.uuid4()),
            "name": self.fake.name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "address": self.fake.address(),
            "created_at": self.fake.date_time_this_year().isoformat(),
        }

    def generate_multi(self, count=10):
        """生成多筆使用者資料"""
        return [self.generate_one() for _ in range(count)]


class PostGenerator(BaseGenerator):
    """文章資料生成器"""

    def generate_one(self):
        """生成單筆文章資料"""
        return {
            "id": str(self.fake.uuid4()),
            "title": self.fake.sentence(nb_words=6, variable_nb_words=True),
            "content": self.fake.text(),
            "author_id": str(self.fake.uuid4()),
            "created_at": self.fake.date_time_this_year().isoformat(),
        }

    def generate_multi(self, count=10):
        """生成多筆文章資料"""
        return [self.generate_one() for _ in range(count)]


class CommentGenerator(BaseGenerator):
    """評論資料生成器"""

    def generate_one(self):
        """生成單筆評論資料"""
        return {
            "id": str(self.fake.uuid4()),
            "content": self.fake.text(),
            "post_id": str(self.fake.uuid4()),
            "author_id": str(self.fake.uuid4()),
            "created_at": self.fake.date_time_this_year().isoformat(),
        }

    def generate_multi(self, count=10):
        """生成多筆評論資料"""
        return [self.generate_one() for _ in range(count)]


class ProductGenerator(BaseGenerator):
    """商品資料生成器"""

    def generate_one(self):
        """生成單筆商品資料"""
        return {
            "id": str(self.fake.uuid4()),
            "name": self.fake.word(),
            "price": self.fake.pyint(min_value=100, max_value=5000),
            "description": self.fake.text(),
            "created_at": self.fake.date_time_this_year().isoformat(),
        }

    def generate_multi(self, count=10):
        """生成多筆商品資料"""
        return [self.generate_one() for _ in range(count)]


class CustomGenerator(BaseGenerator):
    """
    自定義資料生成器
    根據傳入的 schema 定義，動態呼叫 Faker 對應的方法來生成資料
    """

    def __init__(self, schema_definition, locale="zh_TW"):
        super().__init__(locale=locale)
        self.schema_definition = schema_definition

    def generate_one(self):
        """根據 schema_definition 生成單筆資料"""
        result = {}
        # 遍歷 schema 定義的每個欄位
        for field_name, faker_method in self.schema_definition.items():
            # 嘗試從 self.fake 中找到對應的方法，例如 faker_method 是 'uuid4'，就會找到 self.fake.uuid4
            method = getattr(self.fake, faker_method, None)

            if method and callable(method):
                try:
                    # 執行該方法並將結果存入字典
                    result[field_name] = method()
                except Exception:
                    # 如果執行失敗，填入錯誤提示
                    result[field_name] = f"<Error executing {faker_method}>"
            else:
                # 如果 Faker 沒有這個方法，直接把字串當作預設值回傳
                result[field_name] = faker_method

        return result

    # 繼承父類別，generate_multi 已經幫我們實作好了！
