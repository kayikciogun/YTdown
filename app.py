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
        
        # yt-dlp GitHub'dan önerilen ayarlar - 2025 Bot korumasını aşma
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 60,
            'retries': 10,
            'fragment_retries': 10,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android_creator'],  # iOS öncelikli
                    'player_skip': ['webpage', 'js', 'configs'],  # Tüm kontrolleri atla
                    'skip': ['hls', 'dash'],  # Sadece progressive formatlar
                }
            },
            'format': 'bestaudio[ext=m4a]/bestaudio',  # m4a tercih et
        }
        
        # yt-dlp 2025 önerileri - iOS öncelikli + fallback'ler
        methods = [
            # Yöntem 1: iOS Music (en az engellenen)
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['ios_music'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 2: iOS
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['ios'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 3: Android Creator
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['android_creator'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 4: Android Music
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['android_music'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 5: mweb (son çare)
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['mweb'], 'player_skip': ['webpage', 'js', 'configs']}}},
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
        
        # Bot korumasını aşma ayarları - İndirme için (2025 güncel)
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio',  # m4a tercih et
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '0',  # En iyi kalite
            }],
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 60,
            'retries': 10,
            'fragment_retries': 10,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android_creator'],
                    'player_skip': ['webpage', 'js', 'configs'],
                    'skip': ['hls', 'dash'],
                }
            },
        }
        
        # 2025 güncel client'lar ile deneme
        methods = [
            # Yöntem 1: iOS Music (en az engellenen)
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['ios_music'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 2: iOS
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['ios'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 3: Android Creator
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['android_creator'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 4: Android Music
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['android_music'], 'player_skip': ['webpage', 'js', 'configs']}}},
            # Yöntem 5: mweb
            {**ydl_opts, 'extractor_args': {'youtube': {'player_client': ['mweb'], 'player_skip': ['webpage', 'js', 'configs']}}},
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

