# 🚀 YouTube WAV İndirici - Deployment Kılavuzu

## Adım 1: GitHub'a Kod Yükleme

Terminal'de şu komutları çalıştırın:

```bash
cd /Users/mac/Desktop/yt-Down
git push -u origin main
```

**Not:** GitHub size kullanıcı adı ve şifre soracak. 
- Kullanıcı adı: GitHub kullanıcı adınız
- Şifre: Personal Access Token (klasik şifre artık çalışmıyor)

### Personal Access Token Oluşturma:
1. GitHub'da: Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token (classic)" tıklayın
3. "repo" yetkisini seçin
4. Token'ı kopyalayın ve şifre yerine kullanın

## Adım 2: Render'a Deploy (Otomatik)

Kodu GitHub'a pushladıktan sonra, ben otomatik olarak Render'a deploy edeceğim! 🎉

## Oluşturulan Dosyalar:
- ✅ `.gitignore` - Gereksiz dosyaları hariç tut
- ✅ `Procfile` - Render başlatma komutu
- ✅ `runtime.txt` - Python versiyonu
- ✅ `render.yaml` - Render yapılandırması
- ✅ `requirements.txt` - Python bağımlılıkları (gunicorn eklendi)
- ✅ `templates/index.html` - Modern web arayüzü

## Özellikler:
- 🎵 YouTube videoları → WAV formatı
- 🎨 Modern ve kullanıcı dostu arayüz
- 📱 Mobil uyumlu
- ⚡ Hızlı ve güvenilir
- 🌐 Global erişim (deploy sonrası)

---
Hazırladım: AI Assistant 🤖

