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
        
        # JALUR PALING STABIL: Menggunakan model 'gemini-pro' atau 'gemini-1.5-flash'
        # Kita tembak langsung tanpa library agar tidak dipaksa ke v1beta
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}"}]}]
        }

        response = requests.post(url, json=payload)
        res_json = response.json()

        # Jika error karena model, kita ganti otomatis ke model cadangan
        if "error" in res_json and res_json["error"]["code"] == 404:
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
            response = requests.post(url, json=payload)
            res_json = response.json()

        text = res_json['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"hasil": text})
    except Exception as e:
        return jsonify({"error": f"Kontak Google Gagal: {str(e)}"}), 500
