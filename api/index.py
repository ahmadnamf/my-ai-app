import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Environment Variable Vercel nanti
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = f"Buatkan {data['jumlah']} soal {data['tipe']} untuk {data['mapel']} kelas {data['kelas']}. Tingkat kesulitan {data['sulit']}. Sertakan kunci jawaban di akhir."
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return jsonify({"hasil": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500