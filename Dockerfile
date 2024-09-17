FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt && rm -rf /root/.cache/pip

#RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
#    && pip install --upgrade pip && pip install -r requirements.txt \
#    && rm -rf /var/lib/apt/lists/* /root/.cache/pip

COPY . .

RUN chmod a+x /app/docker/*.sh

EXPOSE 8003

#WORKDIR /app/src
#CMD ["gunicorn", "main:main_app", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8003"]

#CMD gunicorn main:main_app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8003

#CMD ["uvocorn", "main:main_app", "--reload", "--host", "0.0.0.0", "--port", "8003"]






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
