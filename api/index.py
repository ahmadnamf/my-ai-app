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
        
        # Kita coba satu model saja yang paling umum: gemini-1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}"}]}]
        }

        response = requests.post(url, json=payload)
        res_json = response.json()

        # CEK: Jika Google mengirimkan error resmi
        if "error" in res_json:
            return jsonify({"error": f"Google bilang: {res_json['error']['message']}"}), 400

        # CEK: Jika Google menolak karena alasan keamanan/sensor
        if "candidates" not in res_json:
            return jsonify({"error": f"Google tidak mengirim jawaban. Respon lengkap: {res_json}"}), 500

        # Jika sukses
        text = res_json['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"hasil": text})

    except Exception as e:
        return jsonify({"error": f"Kesalahan Sistem: {str(e)}"}), 500
