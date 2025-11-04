from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid
from pathlib import Path
import tempfile
import shutil
import time
import random

app = Flask(__name__)

# Geçici indirme klasörü
DOWNLOAD_FOLDER = tempfile.gettempdir()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-info', methods=['POST'])
def get_info():
    """Video bilgilerini al"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL gerekli'}), 400
        
        # yt-dlp GitHub'dan önerilen ayarlar - Bilgi alma için
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'referer': 'https://www.youtube.com/',
            'sleep_interval': random.randint(3, 8),
            'max_sleep_interval': 15,
            'socket_timeout': 60,
            'retries': 5,
            'fragment_retries': 5,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],  # Sadeleştirilmiş
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
        
        # yt-dlp GitHub önerileri - Farklı yöntemler dene
        methods = [
            ydl_opts,  # İlk yöntem - iOS
            {**ydl_opts, 'user_agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'extractor_args': {'youtube': {'player_client': ['android']}}},  # Android
            {**ydl_opts, 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'extractor_args': {'youtube': {'player_client': ['web']}}},  # Windows
        ]
        
        for i, method_opts in enumerate(methods):
            try:
                with yt_dlp.YoutubeDL(method_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    
                    return jsonify({
                        'title': info.get('title', 'Bilinmeyen'),
                        'duration': info.get('duration', 0),
                        'thumbnail': info.get('thumbnail', ''),
                        'channel': info.get('channel', info.get('uploader', 'Bilinmeyen')),
                    })
            except Exception as e:
                if i == len(methods) - 1:  # Son yöntem de başarısız
                    raise e
                time.sleep(3)  # Yöntemler arası bekleme
    
    except Exception as e:
        return jsonify({'error': f'Hata: {str(e)}'}), 400

@app.route('/download', methods=['POST'])
def download():
    """Videoyu WAV formatında indir"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL gerekli'}), 400
        
        # Benzersiz dosya adı oluştur
        unique_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_FOLDER, f'yt_audio_{unique_id}')
        
        # En güçlü bot koruması aşma ayarları - İndirme için (yt-dlp GitHub'dan önerilen format)
        ydl_opts = {
            'format': 'bestaudio*',  # GitHub'da önerilen format - tüm ses formatlarını kabul eder
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0',  # En iyi kalite
            }],
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'referer': 'https://www.youtube.com/',
            'sleep_interval': random.randint(3, 8),
            'max_sleep_interval': 15,
            'socket_timeout': 60,
            'retries': 5,
            'fragment_retries': 5,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web'],  # Sadeleştirilmiş client listesi
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        }
        
        # yt-dlp GitHub'dan önerilen formatlar - bestaudio* tüm ses formatlarını kabul eder
        methods = [
            ydl_opts,  # İlk yöntem - iOS + bestaudio*
            {**ydl_opts, 'format': 'bestaudio*', 'user_agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'extractor_args': {'youtube': {'player_client': ['android']}}},  # Android
            {**ydl_opts, 'format': 'ba*', 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'extractor_args': {'youtube': {'player_client': ['web']}}},  # Windows
        ]
        
        for i, method_opts in enumerate(methods):
            try:
                with yt_dlp.YoutubeDL(method_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio')
                    break
            except Exception as e:
                error_msg = str(e).lower()
                if 'requested format is not available' in error_msg:
                    # Format hatası - alternatif format dene
                    if i < len(methods) - 1:
                        print(f"Format hatası, alternatif yöntem deneniyor... ({i+1}/{len(methods)})")
                        time.sleep(2)
                        continue
                if i == len(methods) - 1:  # Son yöntem de başarısız
                    raise e
                time.sleep(3)  # Yöntemler arası bekleme
        
        # İndirilen dosyayı bul
        wav_file = f"{output_path}.wav"
        
        if not os.path.exists(wav_file):
            return jsonify({'error': 'Dosya indirilemedi'}), 500
        
        # Güvenli dosya adı oluştur
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title[:100]  # Maksimum 100 karakter
        
        return send_file(
            wav_file,
            as_attachment=True,
            download_name=f'{safe_title}.wav',
            mimetype='audio/wav'
        )
    
    except Exception as e:
        return jsonify({'error': f'İndirme hatası: {str(e)}'}), 500
    
    finally:
        # İndirilen dosyaları temizle
        try:
            if 'wav_file' in locals() and os.path.exists(wav_file):
                os.remove(wav_file)
        except:
            pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

