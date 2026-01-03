import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Environment Variable Vercel
api_key = os.environ.get("GEMINI_API_KEY")

# Konfigurasi dengan versi API 'v1' (menghindari masalah v1beta)
genai.configure(api_key=api_key, transport='rest')

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan kunci jawaban."

        # Gunakan nama model yang paling standar saat ini
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"hasil": response.text})
        else:
            return jsonify({"error": "Respon kosong dari AI"}), 500

    except Exception as e:
        # Jika masih gagal, kirim pesan error yang lebih bersih
        return jsonify({"error": str(e)}), 500
