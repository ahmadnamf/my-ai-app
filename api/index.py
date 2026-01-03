import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        data = request.json
        
        # LANGKAH 1: Tanya Google model apa yang AKTIF untuk akun ini
        list_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        list_response = requests.get(list_url)
        models_data = list_response.json()
        
        # Ambil semua model yang mendukung generateContent
        available_models = [
            m["name"] for m in models_data.get("models", []) 
            if "generateContent" in m.get("supportedGenerationMethods", [])
        ]

        if not available_models:
            return jsonify({"error": "Akun Anda tidak memiliki model aktif. Pastikan API Key benar."}), 404

        # LANGKAH 2: Pakai model pertama yang ditemukan
        # Biasanya akan menemukan 'models/gemini-1.5-flash-8b' atau 'models/gemini-pro'
        target_model = available_models[0]
        gen_url = f"https://generativelanguage.googleapis.com/v1/{target_model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan jawaban."}]
            }]
        }

        response = requests.post(gen_url, json=payload)
        result = response.json()
        
        text_output = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({
            "hasil": text_output, 
            "info": f"Berhasil menggunakan model: {target_model}"
        })

    except Exception as e:
        return jsonify({"error": f"Gagal pada tahap deteksi: {str(e)}"}), 500
