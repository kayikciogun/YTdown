# 🚀 YouTube WAV İndirici - Başlatıcı Kılavuzu

## 📱 Nasıl Başlatılır?

### 🍎 macOS Kullanıcıları:

**En Kolay Yöntem:**
1. **`YouTube WAV İndirici.command`** dosyasını **çift tıklayın**
2. Terminal otomatik açılacak ve uygulama başlayacak
3. Tarayıcınızda `http://localhost:5001` adresini açın

**Terminal Yöntemi:**
```bash
./start.sh
```

### 🪟 Windows Kullanıcıları:

**En Kolay Yöntem:**
1. **`start.bat`** dosyasını **çift tıklayın**
2. Komut penceresi açılacak ve uygulama başlayacak
3. Tarayıcınızda `http://localhost:5001` adresini açın

### 🐧 Linux Kullanıcıları:

```bash
./start.sh
```

## 🔧 Gereksinimler

### ✅ Otomatik Kontrol Edilenler:
- **Python 3.7+** - Otomatik kontrol edilir
- **FFmpeg** - Ses dönüştürme için gerekli
- **Python paketleri** - Otomatik yüklenir

### 📦 Manuel Kurulum (Gerekirse):

**macOS:**
```bash
# Python (genellikle zaten kurulu)
brew install python3

# FFmpeg
brew install ffmpeg
```

**Windows:**
- Python: https://www.python.org/downloads/
- FFmpeg: https://ffmpeg.org/download.html

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip ffmpeg
```

## 🎯 Kullanım

### 1️⃣ **Uygulamayı Başlatın**
- macOS: `YouTube WAV İndirici.command` çift tıklayın
- Windows: `start.bat` çift tıklayın
- Linux: `./start.sh` çalıştırın

### 2️⃣ **Tarayıcıda Açın**
```
http://localhost:5001
```

### 3️⃣ **Video İndirin**
1. YouTube video URL'sini kopyalayın
2. URL'yi giriş kutusuna yapıştırın
3. "Bilgi Al" butonuna tıklayın
4. "WAV Olarak İndir" butonuna tıklayın
5. Dosya otomatik indirilecek!

## 🛑 Durdurma

**Terminal/Komut penceresinde:**
- `Ctrl + C` tuşlarına basın

## 🔍 Sorun Giderme

### ❌ "Python bulunamadı" Hatası:
- Python 3.7+ kurun
- PATH'e eklendiğinden emin olun

### ❌ "FFmpeg bulunamadı" Hatası:
- FFmpeg kurun
- macOS: `brew install ffmpeg`
- Windows: https://ffmpeg.org/download.html

### ❌ "Port 5001 kullanımda" Hatası:
- Eski sunucu otomatik durdurulur
- Manuel durdurmak için: `pkill -f "python3 app.py"`

### ❌ "403 Forbidden" Hatası:
- Normal! Sistem otomatik olarak farklı yöntemler dener
- Biraz bekleyin, genellikle 2. denemede başarılı olur

## 💡 İpuçları

### 🎵 En İyi Sonuçlar:
- **Müzik videoları** en hızlı indirilir
- **Kısa videolar** (1-5 dakika) daha az süre alır
- **Popüler videolar** daha az kısıtlama var
- **Eski videolar** daha az bot koruması var

### ⚡ Hızlandırma:
- Aynı tür videolar daha hızlı indirilir
- Sistem öğrenir ve cache kullanır
- İnternet hızınız etkiler

### 🎯 Kalite:
- **WAV formatı** - Kayıpsız, en yüksek kalite
- **Büyük dosya boyutu** - Yüksek kalite = büyük dosya
- **Profesyonel kalite** - Müzik prodüksiyonu için uygun

## 📞 Destek

Sorun yaşarsanız:
1. **Gereksinimleri kontrol edin** (Python, FFmpeg)
2. **Port 5001'i kontrol edin** (başka uygulama kullanıyor olabilir)
3. **Farklı video deneyin** (müzik videoları daha iyi çalışır)
4. **İnternet bağlantınızı kontrol edin**

---

**Keyifli kullanımlar! 🎵✨**


