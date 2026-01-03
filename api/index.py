import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Environment Variable Vercel
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        prompt = f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan kunci jawaban."

        # DAFTAR MODEL UNTUK DICOBA (Urutan dari yang paling mungkin berhasil)
        # Gunakan 'gemini-1.5-flash-latest' atau 'gemini-1.0-pro'
        model_names = ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-pro"]
        
        response_text = None
        error_msg = ""

        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                response = model.generate_content(prompt)
                response_text = response.text
                if response_text:
                    break
            except Exception as e:
                error_msg = str(e)
                continue

        if response_text:
            return jsonify({"hasil": response_text})
        else:
            return jsonify({"error": f"Model tidak ditemukan di wilayah ini. Detail: {error_msg}"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
