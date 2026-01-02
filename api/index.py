import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Konfigurasi Gemini AI
# Pastikan Anda sudah menambahkan GEMINI_API_KEY di Environment Variables Vercel
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate_questions():
    try:
        data = request.json
        subject = data.get('mapel', 'Umum')
        grade = data.get('kelas', 'SMP/SMA')
        count = data.get('jumlah', 5)
        level = data.get('sulit', 'Sedang')
        q_type = data.get('tipe', 'Pilihan Ganda')

        # Prompt instruksi untuk Gemini
        prompt = (
            f"Buatkan {count} soal {q_type} untuk mata pelajaran {subject} "
            f"kelas {grade} dengan tingkat kesulitan {level}. "
            f"Berikan jawaban yang jelas di bagian bawah setiap soal."
        )

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return jsonify({"hasil": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Penting: Jangan gunakan app.run() agar kompatibel dengan Vercel Serverless
