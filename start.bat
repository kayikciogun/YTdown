@echo off
chcp 65001 >nul
title YouTube WAV İndirici

echo.
echo 🎵 YouTube WAV İndirici Başlatılıyor...
echo ==================================

REM Python kontrolü
echo 📋 Python kontrolü yapılıyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python kurun.
    pause
    exit /b 1
)

REM FFmpeg kontrolü
echo 🎬 FFmpeg kontrolü yapılıyor...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  FFmpeg bulunamadı! Ses dönüştürme için gerekli.
    echo    Kurulum: https://ffmpeg.org/download.html
    echo.
    set /p continue="Devam etmek istiyor musunuz? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

REM Gerekli paketleri kontrol et
echo 📦 Python paketleri kontrol ediliyor...
if not exist "requirements.txt" (
    echo ❌ requirements.txt bulunamadı!
    pause
    exit /b 1
)

REM Paketleri yükle
echo ⬇️  Gerekli paketler yükleniyor...
pip install -r requirements.txt --quiet

REM Port kontrolü
echo 🔌 Port kontrolü yapılıyor...
netstat -an | find "5001" >nul
if not errorlevel 1 (
    echo ⚠️  Port 5001 kullanımda! Eski sunucu durduruluyor...
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 2 >nul
)

REM Sunucuyu başlat
echo 🚀 YouTube WAV İndirici başlatılıyor...
echo ✅ Sunucu hazır!
echo.
echo 🌐 Tarayıcınızda şu adresi açın:
echo    http://localhost:5001
echo.
echo 🛑 Durdurmak için Ctrl+C tuşlarına basın
echo ==================================
echo.

REM Flask sunucusunu arka planda başlat
echo 🚀 Sunucu başlatılıyor...
start /b python app.py

REM Sunucunun hazır olmasını bekle
echo ⏳ Sunucu hazır olması bekleniyor...
timeout /t 3 >nul

REM Tarayıcıyı aç
echo 🌐 Tarayıcı açılıyor...
start http://localhost:5001

REM Sunucuyu bekle
echo ✅ Sunucu çalışıyor! Tarayıcıda kullanabilirsiniz.
echo 🛑 Durdurmak için bu pencereyi kapatın
pause
