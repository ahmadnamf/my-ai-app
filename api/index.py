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
        # Gunakan 'gemini-pro' untuk menghindari error 404 model not found
        model = genai.GenerativeModel("gemini-pro")
        
        prompt = (f"Buatkan {data.get('jumlah')} soal {data.get('tipe')} "
                  f"mata pelajaran {data.get('mapel')} kelas {data.get('kelas')}. "
                  f"Sertakan kunci jawaban di akhir.")

        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"hasil": response.text})
        else:
            return jsonify({"error": "AI tidak memberikan respon"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
