FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV JARVIS_DB=/data/jarvis.db \
    JARVIS_OUT=/data/documents \
    JARVIS_PIN=4435

RUN mkdir -p /data/documents

EXPOSE 8080

CMD ["uvicorn", "jarvis_api:app", "--host", "0.0.0.0", "--port", "8080"]
