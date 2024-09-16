# Используем официальный базовый образ Python
FROM python:3.12.3-slim

# Устанавливаем необходимые зависимости для Poetry и компиляции
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*  # Очистка кэша apt

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . .

# Запускаем приложение
CMD ["uvicorn", "src.main:main_app", "--host", "0.0.0.0", "--port", "8000"]
