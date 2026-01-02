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
        mapel = data.get('mapel', 'Umum')
        kelas = data.get('kelas', 'SMP/SMA')
        jumlah = data.get('jumlah', 5)
        sulit = data.get('sulit', 'Sedang')
        tipe = data.get('tipe', 'Pilihan Ganda')

        # Ganti ke model yang paling didukung secara global
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
        prompt = (
            f"Buatkan {jumlah} soal {tipe} untuk mata pelajaran {mapel} "
            f"kelas {kelas} dengan tingkat kesulitan {sulit}. "
            f"Berikan jawaban di bagian paling bawah."
        )

        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"hasil": response.text})
        else:
            return jsonify({"error": "Respon kosong dari AI"}), 500

    except Exception as e:
        # Jika gemini-1.5-flash masih error, otomatis coba pakai gemini-pro
        try:
            model_backup = genai.GenerativeModel("gemini-pro")
            response = model_backup.generate_content(prompt)
            return jsonify({"hasil": response.text})
        except:
            return jsonify({"error": str(e)}), 500

# Standar Vercel: Tidak perlu app.run()
