FROM python:3.9-slim

# Systempakete installieren (einschließlich ffmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean

# Arbeitsverzeichnis setzen
WORKDIR /app

# requirements.txt zuerst kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Rest der Anwendung kopieren
COPY . .

# Startbefehl
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]