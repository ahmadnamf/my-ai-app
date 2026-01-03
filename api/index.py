import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Konfigurasi API
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}"

        # Coba gunakan gemini-pro (Paling stabil untuk semua wilayah)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        
        return jsonify({"hasil": response.text})
    except Exception as e:
        # Jika gemini-pro juga gagal, tampilkan error aslinya
        return jsonify({"error": str(e)}), 500
