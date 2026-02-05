# 使用官方 Python 3.13 運行時作為基礎映像（匹配本地 3.13.6 環境）
FROM python:3.13-slim

# 設置環境變數
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
  gcc \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# 安裝 Python 依賴
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 複製專案檔案
COPY . /app/

# 收集靜態檔案（如果需要）
# RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 啟動命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
