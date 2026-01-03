import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai.types import RequestOptions

app = Flask(__name__)
CORS(app)

# Ambil API Key
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = f"Buatkan 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan kunci jawaban."

        # PAKSA menggunakan API v1 dan model terbaru
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Menggunakan RequestOptions untuk memastikan versi v1
        response = model.generate_content(
            prompt,
            request_options=RequestOptions(api_version='v1')
        )
        
        return jsonify({"hasil": response.text})
    except Exception as e:
        # Menampilkan detail error agar kita tahu jika masih memanggil v1beta
        return jsonify({"error": str(e)}), 500
