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
        prompt = f"Buatkan {data.get('jumlah')} soal {data.get('tipe')} {data.get('mapel')} kelas {data.get('kelas')} kesulitan {data.get('sulit')}. Sertakan kunci jawaban."

        # Strategi 1: Coba model terbaru
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return jsonify({"hasil": response.text})
        except Exception as e:
            # Strategi 2: Jika gagal (karena library jadul), gunakan model Pro yang lebih stabil
            print(f"Flash gagal, mencoba Pro: {str(e)}")
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return jsonify({"hasil": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
