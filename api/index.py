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
        # Gunakan model generik 'gemini-pro' atau 'gemini-1.5-flash'
        # Cobalah ganti ke 'gemini-pro' jika 'flash' tetap 404
        model = genai.GenerativeModel("gemini-pro")
        
        prompt = f"Buatkan 5 soal {data.get('mapel')} kelas {data.get('kelas')}. Berikan kunci jawabannya."
        
        response = model.generate_content(prompt)
        
        return jsonify({"hasil": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
