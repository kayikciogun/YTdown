# 🎵 YouTube WAV İndirici

Modern ve kullanıcı dostu tarayıcı tabanlı YouTube ses indirme aracı. En yüksek kalitede ses dosyalarını WAV formatında indirin.

## ✨ Özellikler

- 🎯 **En İyi Kalite**: YouTube'dan mevcut en yüksek ses kalitesini indirir
- 🎼 **WAV Format**: Kayıpsız, profesyonel kalitede WAV formatında
- ⚡ **Hızlı ve Kolay**: Sadece URL'yi yapıştırın ve indirin
- 🎨 **Modern Arayüz**: Responsive ve kullanıcı dostu tasarım
- 📱 **Mobil Uyumlu**: Tüm cihazlarda mükemmel çalışır
- 🔧 **Akıllı Format Seçimi**: yt-dlp GitHub'dan önerilen `bestaudio*` formatı
- 🛡️ **Bot Koruması Aşma**: 3 farklı yöntem ile maksimum uyumluluk

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- FFmpeg (ses dönüştürme için gerekli)

## 🚀 Kurulum

1. **Repoyu klonlayın veya dosyaları indirin**

2. **FFmpeg kurun**:
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **Windows:**
   [FFmpeg resmi sitesinden](https://ffmpeg.org/download.html) indirin ve PATH'e ekleyin

3. **Python paketlerini kurun**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Kullanım

1. **Uygulamayı başlatın**:
   ```bash
   python app.py
   ```

2. **Tarayıcınızda açın**:
   ```
   http://localhost:5000
   ```

3. **YouTube videosunu indirin**:
   - YouTube video URL'sini kopyalayın
   - URL'yi giriş kutusuna yapıştırın
   - "Bilgi Al" butonuna tıklayın
   - Video bilgilerini kontrol edin
   - "WAV Olarak İndir" butonuna tıklayın
   - Dosya otomatik olarak indirilecek

## 📁 Proje Yapısı

```
.
├── app.py                 # Flask backend uygulaması
├── requirements.txt       # Python bağımlılıkları
├── README.md             # Bu dosya
├── templates/
│   └── index.html        # Ana HTML sayfası
└── static/
    ├── style.css         # CSS stilleri
    └── script.js         # JavaScript kodu
```

## 🛠️ Teknik Detaylar

- **Backend**: Flask (Python)
- **Video İndirme**: yt-dlp (2025.9.26+)
- **Ses Dönüştürme**: FFmpeg
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Ses Formatı**: WAV (en yüksek kalite, kayıpsız)
- **Format Seçimi**: `bestaudio*` (GitHub önerilen format - tüm ses formatlarını kabul eder)
- **Bot Koruması**: 3 farklı player client (iOS, Android, Web)

## ⚠️ Önemli Notlar

- Bu araç yalnızca telif hakkı izni olan içerikleri indirmek için kullanılmalıdır
- İndirme hızı internet bağlantınıza ve videonun uzunluğuna bağlıdır
- WAV dosyaları yüksek kaliteli ancak büyük boyutludur
- FFmpeg kurulumu zorunludur

## 📝 Lisans

Bu proje eğitim amaçlıdır. Lütfen telif haklarına saygı gösterin.

## 🤝 Katkıda Bulunma

Öneriler ve geliştirmeler için katkıda bulunabilirsiniz!

## 🐛 Sorun Giderme

**"FFmpeg bulunamadı" hatası alıyorsanız:**
- FFmpeg'in kurulu olduğundan emin olun
- FFmpeg'in PATH'e eklendiğini kontrol edin

**İndirme başarısız oluyorsa:**
- URL'nin doğru olduğundan emin olun
- İnternet bağlantınızı kontrol edin
- Video erişilebilir durumda olmalı (özel veya kısıtlı değil)

**Sunucu başlatılamıyorsa:**
- 5000 portunun kullanımda olmadığından emin olun
- Gerekli Python paketlerinin kurulu olduğunu kontrol edin

## 📞 Destek

Sorun yaşarsanız veya önerileriniz varsa lütfen iletişime geçin.

---

Yapımcı ile ❤️ türkçe destek

