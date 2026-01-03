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
        # Masukkan API Key asli Anda di sini
        api_key = "AIzaSyDkU543vmAtz-WqzdnDRgU9a35ml6TYgp8" 
        
        # Kita paksa langsung ke model gemini-1.5-flash
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}"}]}]
        }

        response = requests.post(url, json=payload)
        res_json = response.json()

        # Jika Google memberikan error, kita tampilkan pesan error aslinya di sini
        if "error" in res_json:
            return jsonify({"error": f"Pesan asli Google: {res_json['error']['message']}"}), 400

        text = res_json['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"hasil": text})
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500
