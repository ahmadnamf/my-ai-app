import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Environment Variables
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate_questions():
    try:
        data = request.json
        prompt = (f"Buatkan {data.get('jumlah')} soal {data.get('tipe')} "
                  f"{data.get('mapel')} kelas {data.get('kelas')} "
                  f"kesulitan {data.get('sulit')}. Sertakan kunci jawaban.")

        # DAFTAR MODEL YANG AKAN DICOBA (Dari yang terbaru ke paling stabil)
        available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        
        response_text = ""
        last_error = ""

        for model_name in available_models:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                response_text = response.text
                if response_text:
                    break # Berhasil, keluar dari loop
            except Exception as e:
                last_error = str(e)
                continue # Coba model berikutnya jika 404

        if response_text:
            return jsonify({"hasil": response_text})
        else:
            return jsonify({"error": f"Semua model gagal. Error terakhir: {last_error}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
