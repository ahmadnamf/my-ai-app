import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # JALUR PRODUKSI STABIL (Bukan v1beta)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan jawaban."}]
            }]
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": f"Google API Error: {response.text}"}), response.status_code

        result = response.json()
        # Mengambil teks hasil generate dari struktur JSON Google
        text_output = result['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({"hasil": text_output})

    except Exception as e:
        return jsonify({"error": f"Sistem gagal: {str(e)}"}), 500
