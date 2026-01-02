import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Vercel Environment Variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = f"Buatkan {data.get('jumlah')} soal {data.get('tipe')} {data.get('mapel')} kelas {data.get('kelas')} kesulitan {data.get('sulit')}. Sertakan kunci jawaban."

        # Gunakan model 'gemini-pro' jika 'gemini-1.5-flash' bermasalah di versi lama
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return jsonify({"hasil": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
