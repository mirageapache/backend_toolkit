from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultSetPagination(PageNumberPagination):
    """
    標準分頁格式
    """

    page_size = 10  # 預設每頁顯示 10 筆
    page_size_query_param = "size"  # 讓前端可以自訂每頁幾筆 (例如 size=50)
    max_page_size = 100  # 最大每頁顯示 100 筆

    def get_paginated_response(self, data):
        # 可自定義回傳的 JSON 格式
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data,
            }
        )
