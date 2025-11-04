# Python 3.12 base image
FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle (FFmpeg dahil)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port'u belirt
EXPOSE 10000

# Gunicorn ile uygulamayı başlat
CMD gunicorn --bind 0.0.0.0:10000 --workers 2 --timeout 120 app:app

