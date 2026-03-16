from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    自定義例外處理器
    格式化錯誤訊息，確保 API 回傳一致的 JSON 格式
    """
    # 呼叫 DRF 預設的例外處理
    response = exception_handler(exc, context)

    if response is not None:
        # 修改回傳結構
        response.data = {
            "error": {
                "code": response.status_code,
                "message": str(exc),
                "details": response.data,
            }
        }

    return response
