import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Pastikan API KEY sudah ada di Environment Variables Vercel
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        # Ambil data dari frontend
        mapel = data.get('mapel', 'Umum')
        kelas = data.get('kelas', 'SMP/SMA')
        jumlah = data.get('jumlah', 5)
        sulit = data.get('sulit', 'Sedang')
        tipe = data.get('tipe', 'Pilihan Ganda')

        # Gunakan 'gemini-1.5-flash' (Jika tetap error, ganti ke 'gemini-pro')
        model = model = genai.GenerativeModel("gemini-pro")
        
        prompt = (
            f"Buatkan {jumlah} soal {tipe} untuk mata pelajaran {mapel} "
            f"kelas {kelas} dengan tingkat kesulitan {sulit}. "
            f"Sertakan kunci jawaban di akhir soal."
        )

        response = model.generate_content(prompt)
        
        # Cek apakah ada hasil teks
        if response.text:
            return jsonify({"hasil": response.text})
        else:
            return jsonify({"error": "AI tidak memberikan respon teks."}), 500

    except Exception as e:
        # Menampilkan error spesifik di log jika terjadi kegagalan
        print(f"Detail Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

