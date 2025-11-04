# 🎵 YouTube WAV İndirici - Kullanım Kılavuzu

## ⚠️ ÖNEMLİ: YouTube'un 2024-2025 Bot Koruması

YouTube artık cloud sunuculardan (Render, Heroku, etc.) gelen istekleri çok sıkı kontrol ediyor ve **PO Token** gerektiriyor. Bu yüzden online deployment tam olarak çalışmayabilir.

## ✅ ÖNERİLEN KULLANIM: Local (Kendi Bilgisayarınız)

### Adım 1: Uygulamayı Başlatın

```bash
cd /Users/mac/Desktop/yt-Down
python3 app.py
```

### Adım 2: Tarayıcıda Açın

http://localhost:5001

### Adım 3: Kullanın!

- YouTube video URL'sini yapıştırın
- "Video Bilgisi Al" veya direkt "İndir" butonuna tıklayın
- WAV dosyanız indirilecek!

## 🌐 Online Deployment (Render)

Render'da deploy edildi ama YouTube'un bot koruması nedeniyle çalışmayabilir. 

**Deployment URL:** https://youtube-wav-downloader.onrender.com

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler:
- **Flask** - Web framework
- **yt-dlp** - YouTube indirme (en güncel version)
- **FFmpeg** - Audio dönüştürme
- **mweb client** - YouTube bot koruması bypass

### Bot Koruması Aşma Teknikleri:
- ✅ mweb client (mobil web - PO Token gerektirmiyor)
- ✅ Rate limiting (8 saniye gecikme)
- ✅ 4 farklı fallback client
- ✅ Akıllı hata yönetimi
- ✅ Otomatik retry mekanizması

### Bilinen Sınırlamalar:
- YouTube rate limit: ~300 video/saat (guest)
- Cloud sunucular (Render) çoğu videoda engellenebilir
- Bazı videolar PO Token gerektirebilir

## 🆘 Sorun Giderme

### "Sign in to confirm you're not a bot" Hatası

**Neden:** YouTube bot koruması

**Çözümler:**
1. **Local kullanın** (en kolay - yukarıdaki adımlar)
2. 5-10 dakika bekleyip tekrar deneyin
3. Farklı bir video deneyin
4. PO Token ekleyin (gelişmiş)

### PO Token Nasıl Eklenir? (Gelişmiş)

1. [yt-dlp PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide) takip edin
2. PO Token ve Visitor Data'yı alın
3. `app.py` dosyasına ekleyin:

```python
'extractor_args': {
    'youtube': {
        'player_client': ['mweb'],
        'player_skip': ['webpage', 'js', 'configs'],
        'po_token': 'YOUR_PO_TOKEN_HERE',
        'visitor_data': 'YOUR_VISITOR_DATA_HERE'
    }
}
```

## 📊 Rate Limiting

Uygulama otomatik olarak YouTube rate limit'ini aşmamak için her istek arası **8 saniye** bekler.

## 🎯 En İyi Pratikler

1. **Local kullanın** - En güvenilir
2. Çok sık indirme yapmayın
3. Bir video başarısız olursa 5-10 dakika bekleyin
4. Farklı videolar test edin

## 💡 Alternatif Çözümler

YouTube'un koruması çok güçlü olduğu için:

1. **yt-dlp komut satırı** kullanın (doğrudan):
```bash
yt-dlp -x --audio-format wav "VIDEO_URL"
```

2. **Browser extension** kullanın (PO Token otomatik)

3. **VPN** ile farklı IP deneyin

## 📝 Notlar

- Bu uygulama sadece eğitim amaçlıdır
- YouTube'un kullanım şartlarına uyun
- Telif haklı içerikleri indirmeyin
- Kişisel kullanım için sınırlı tutun

---

Made with ❤️ - 2025

