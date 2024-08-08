FROM python:slim
COPY requirements.txt requirements.txt
#RUN #pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app/src
#EXPOSE 8000

CMD ["uvicorn", "main:main_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]