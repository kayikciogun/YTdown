from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import uuid
from pathlib import Path
import tempfile
import shutil
import time
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Geçici indirme klasörü
DOWNLOAD_FOLDER = tempfile.gettempdir()

# Rate limiting için
last_request_time = None
REQUEST_DELAY = 8  # YouTube rate limit için 8 saniye gecikme

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-info', methods=['POST'])
def get_info():
    """Video bilgilerini al"""
    global last_request_time
    
    # Rate limiting - YouTube rate limit aşımını önle
    if last_request_time:
        elapsed = (datetime.now() - last_request_time).total_seconds()
        if elapsed < REQUEST_DELAY:
            wait_time = REQUEST_DELAY - elapsed
            time.sleep(wait_time)
    
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL gerekli'}), 400
        
        last_request_time = datetime.now()
        
        # yt-dlp - PO Token olmadan çalışan ayarlar (2025)
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 90,
            'retries': 15,
            'fragment_retries': 15,
            'extractor_args': {
                'youtube': {
                    'player_client': ['mweb', 'ios'],  # PO Token gerektirmeyen client'lar
                    'player_skip': ['webpage', 'js', 'configs'],
                }
            },
            'format': 'bestaudio',
        }
        
        # PO Token gerektirmeyen client'lar (2025 - Wiki önerisi)
        methods = [
            # Yöntem 1: mweb (mobile web - PO Token yok, Wiki önerisi)
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['mweb'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 2: iOS (genelde PO Token gerektirmiyor)
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['ios'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 3: Android Embedded
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['android_embedded'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 4: TV Embedded
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['tv_embedded'], 'player_skip': ['webpage', 'js', 'configs']}}},
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
                error_msg = str(e).lower()
                if 'sign in to confirm' in error_msg or 'bot' in error_msg:
                    # Bot koruması - daha uzun bekle
                    if i < len(methods) - 1:
                        time.sleep(10)
                        continue
                if i == len(methods) - 1:  # Son yöntem de başarısız
                    raise e
                time.sleep(5)  # Yöntemler arası bekleme
    
    except Exception as e:
        return jsonify({'error': f'Hata: {str(e)}'}), 400

@app.route('/download', methods=['POST'])
def download():
    """Videoyu WAV formatında indir"""
    global last_request_time
    
    # Rate limiting
    if last_request_time:
        elapsed = (datetime.now() - last_request_time).total_seconds()
        if elapsed < REQUEST_DELAY:
            wait_time = REQUEST_DELAY - elapsed
            time.sleep(wait_time)
    
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL gerekli'}), 400
        
        last_request_time = datetime.now()
        
        # Benzersiz dosya adı oluştur
        unique_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOAD_FOLDER, f'yt_audio_{unique_id}')
        
        # PO Token olmadan indirme (2025 - Wiki önerisi)
        ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0',  # En iyi kalite
            }],
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 90,
            'retries': 15,
            'fragment_retries': 15,
            'extractor_args': {
                'youtube': {
                    'player_client': ['mweb', 'ios'],
                    'player_skip': ['webpage', 'js', 'configs'],
                }
            },
        }
        
        # PO Token gerektirmeyen client'lar (Wiki önerisi)
        methods = [
            # Yöntem 1: mweb (mobile web - PO Token yok)
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['mweb'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 2: iOS
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['ios'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 3: Android Embedded
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['android_embedded'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 4: TV Embedded
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['tv_embedded'], 'player_skip': ['webpage', 'js', 'configs']}}},
        ]
        
        for i, method_opts in enumerate(methods):
            try:
                with yt_dlp.YoutubeDL(method_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio')
                    break
            except Exception as e:
                error_msg = str(e).lower()
                if 'sign in to confirm' in error_msg or 'bot' in error_msg:
                    # Bot koruması - daha uzun bekle
                    if i < len(methods) - 1:
                        print(f"Bot koruması algılandı, alternatif client deneniyor... ({i+1}/{len(methods)})")
                        time.sleep(12)
                        continue
                if 'requested format is not available' in error_msg:
                    # Format hatası - alternatif format dene
                    if i < len(methods) - 1:
                        print(f"Format hatası, alternatif yöntem deneniyor... ({i+1}/{len(methods)})")
                        time.sleep(3)
                        continue
                if i == len(methods) - 1:  # Son yöntem de başarısız
                    raise e
                time.sleep(6)  # Yöntemler arası bekleme
        
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

