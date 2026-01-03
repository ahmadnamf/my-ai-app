import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key
api_key = os.environ.get("GEMINI_API_KEY")

# PAKSA konfigurasi ke versi v1 secara global
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = f"Buatkan 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan kunci jawaban."

        # Gunakan model gemini-1.5-flash
        # Jika masih 404, Anda bisa menggantinya ke "gemini-1.5-flash-8b" (lebih ringan)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Panggil tanpa RequestOptions yang bermasalah tadi
        response = model.generate_content(prompt)
        
        return jsonify({"hasil": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
