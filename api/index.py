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
        
        # Daftar model yang akan dicoba secara berurutan
        models_to_try = ["gemini-1.5-flash-8b", "gemini-pro"]
        
        for model_name in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1/models/{model_name}:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan jawaban."}]
                }]
            }

            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                text_output = result['candidates'][0]['content']['parts'][0]['text']
                return jsonify({"hasil": text_output})
        
        # Jika semua model di atas gagal
        return jsonify({"error": f"Semua model gagal. Error terakhir: {response.text}"}), 404

    except Exception as e:
        return jsonify({"error": f"Sistem gagal: {str(e)}"}), 500
