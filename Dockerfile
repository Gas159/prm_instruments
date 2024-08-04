FROM python:slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "server/main:app", "--host", "0.0.0.0", "--port", "8000"]