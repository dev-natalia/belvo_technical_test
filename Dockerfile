FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

EXPOSE 8001

CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8001"]
