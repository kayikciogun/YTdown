#!/bin/bash

# YouTube WAV İndirici - macOS Başlatıcı
# Çift tıklayarak çalıştırılabilir

# Terminal penceresini açık tut
osascript -e 'tell application "Terminal" to activate'

# Renkli çıktı
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

clear
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎵 YouTube WAV İndirici                    ║"
echo "║                        En İyi Kalite                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Çalışma dizinini değiştir
cd "$(dirname "$0")"

echo -e "${BLUE}📁 Çalışma dizini: $(pwd)${NC}"
echo ""

# Python kontrolü
echo -e "${BLUE}🐍 Python kontrolü...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 bulunamadı!${NC}"
    echo -e "${YELLOW}   Kurulum: https://www.python.org/downloads/${NC}"
    echo ""
    read -p "Devam etmek istiyor musunuz? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ Python3 hazır${NC}"
fi

# FFmpeg kontrolü
echo -e "${BLUE}🎬 FFmpeg kontrolü...${NC}"
if ! command -v ffmpeg &> /dev/null; then
    echo -e "${YELLOW}⚠️  FFmpeg bulunamadı!${NC}"
    echo -e "${YELLOW}   Kurulum: brew install ffmpeg${NC}"
    echo ""
    read -p "Devam etmek istiyor musunuz? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ FFmpeg hazır${NC}"
fi

# Paket kontrolü
echo -e "${BLUE}📦 Python paketleri kontrol ediliyor...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt bulunamadı!${NC}"
    exit 1
fi

# Paketleri yükle
echo -e "${BLUE}⬇️  Gerekli paketler yükleniyor...${NC}"
pip3 install -r requirements.txt --quiet --upgrade

# Port kontrolü
echo -e "${BLUE}🔌 Port kontrolü...${NC}"
if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${YELLOW}⚠️  Port 5001 kullanımda! Eski sunucu durduruluyor...${NC}"
    pkill -f "python3 app.py" 2>/dev/null || true
    sleep 2
fi

# Sunucuyu başlat
echo ""
echo -e "${GREEN}🚀 YouTube WAV İndirici başlatılıyor...${NC}"
echo -e "${GREEN}✅ Sunucu hazır!${NC}"
echo ""
echo -e "${YELLOW}🌐 Tarayıcınızda şu adresi açın:${NC}"
echo -e "${BLUE}   http://localhost:5001${NC}"
echo ""
echo -e "${YELLOW}💡 İpuçları:${NC}"
echo -e "${YELLOW}   • Müzik videoları en hızlı indirilir${NC}"
echo -e "${YELLOW}   • Kısa videolar daha az süre alır${NC}"
echo -e "${YELLOW}   • Popüler videolar daha az kısıtlama var${NC}"
echo ""
echo -e "${YELLOW}🛑 Durdurmak için Ctrl+C tuşlarına basın${NC}"
echo ""

# Flask sunucusunu arka planda başlat
echo -e "${GREEN}🚀 Sunucu başlatılıyor...${NC}"
python3 app.py &
SERVER_PID=$!

# Sunucunun hazır olmasını bekle
echo -e "${BLUE}⏳ Sunucu hazır olması bekleniyor...${NC}"
for i in {1..15}; do
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

# Sunucu durduğunda
echo ""
echo -e "${RED}👋 YouTube WAV İndirici durduruldu${NC}"
echo -e "${YELLOW}   Tekrar başlatmak için bu dosyayı çift tıklayın${NC}"
echo ""
read -p "Çıkmak için Enter tuşuna basın..."
