import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Konfigurasi API Key
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

        # Gunakan nama model 'gemini-pro' untuk stabilitas lebih tinggi
        # atau pastikan penulisan 'gemini-1.5-flash' sudah benar
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = (
            f"Buatkan {count} soal {q_type} untuk mata pelajaran {subject} "
            f"kelas {grade} dengan tingkat kesulitan {level}. "
            f"Sertakan kunci jawaban di bagian akhir."
        )

        # Tambahkan konfigurasi safety agar tidak terblokir
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"hasil": response.text})
        else:
            return jsonify({"error": "Gemini tidak memberikan respon. Coba ganti topik."}), 500

    except Exception as e:
        # Menampilkan pesan error yang lebih detail di log Vercel
        print(f"Error Detail: {str(e)}")
        return jsonify({"error": str(e)}), 500
