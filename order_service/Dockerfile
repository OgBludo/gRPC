FROM python:3.10-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование .proto файлов и исходного кода
COPY proto/ ./proto/
COPY . .

# Генерация файлов gRPC
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/order.proto

# Запуск сервиса
CMD ["python", "order_service.py"]
