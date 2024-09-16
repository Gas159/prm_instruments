FROM python:slim
COPY requirements.txt requirements.txt
#RUN #pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app/src
#EXPOSE 8000

CMD ["uvicorn", "main:main_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]





## Используем официальный базовый образ Python
#FROM python:3.12.3-slim
#
## Устанавливаем необходимые зависимости для Poetry и компиляции
#RUN apt-get update && apt-get install -y \
#    curl \
#    build-essential \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*  # Очистка кэша apt
#
## Создаем рабочую директорию
#WORKDIR /app
#
## Копируем файл requirements.txt
#COPY requirements.txt .
#
## Устанавливаем зависимости
#RUN pip install --no-cache-dir -r requirements.txt
#
## Копируем файлы проекта
#COPY . .
#EXPOSE 8001
#WORKDIR /app/src
## Запускаем приложение
#CMD ["uvicorn", "main:main_app", "--host", "0.0.0.0", "--port", "8001"]
