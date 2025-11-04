#!/bin/bash

# YouTube WAV İndirici - Başlatıcı Script
# macOS için optimize edilmiş

echo "🎵 YouTube WAV İndirici Başlatılıyor..."
echo "=================================="

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Python kontrolü
echo -e "${BLUE}📋 Python kontrolü yapılıyor...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 bulunamadı! Lütfen Python3 kurun.${NC}"
    exit 1
fi

# FFmpeg kontrolü
echo -e "${BLUE}🎬 FFmpeg kontrolü yapılıyor...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}⚠️  FFmpeg bulunamadı! Ses dönüştürme için gerekli.${NC}"
    echo -e "${YELLOW}   Kurulum: brew install ffmpeg${NC}"
    echo ""
    read -p "Devam etmek istiyor musunuz? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Gerekli paketleri kontrol et
echo -e "${BLUE}📦 Python paketleri kontrol ediliyor...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt bulunamadı!${NC}"
    exit 1
fi

# Paketleri yükle
echo -e "${BLUE}⬇️  Gerekli paketler yükleniyor...${NC}"
pip3 install -r requirements.txt --quiet

# Port kontrolü
echo -e "${BLUE}🔌 Port kontrolü yapılıyor...${NC}"
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Port 5001 kullanımda! Eski sunucu durduruluyor...${NC}"
    pkill -f "python3 app.py" 2>/dev/null || true
    sleep 2
fi

# Sunucuyu başlat
echo -e "${GREEN}🚀 YouTube WAV İndirici başlatılıyor...${NC}"
echo -e "${GREEN}✅ Sunucu hazır!${NC}"
echo ""
echo -e "${YELLOW}🌐 Tarayıcınızda şu adresi açın:${NC}"
echo -e "${BLUE}   http://localhost:5001${NC}"
echo ""
echo -e "${YELLOW}🛑 Durdurmak için Ctrl+C tuşlarına basın${NC}"
echo "=================================="

# Flask sunucusunu arka planda başlat
echo -e "${GREEN}🚀 Sunucu başlatılıyor...${NC}"
python3 app.py &
SERVER_PID=$!

# Sunucunun hazır olmasını bekle
echo -e "${BLUE}⏳ Sunucu hazır olması bekleniyor...${NC}"
for i in {1..10}; do
    if curl -s http://localhost:5001 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Sunucu hazır!${NC}"
        break
    fi
    sleep 1
done

# Tarayıcıyı aç
echo -e "${GREEN}🌐 Tarayıcı açılıyor...${NC}"
open http://localhost:5001

# Sunucuyu ön planda çalıştır
wait $SERVER_PID
