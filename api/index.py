import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Ambil API Key dari Environment Variable
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        # Gunakan model 'gemini-1.5-flash' yang paling umum
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"Buat 3 soal {data.get('mapel')} kelas {data.get('kelas')}. Sertakan jawaban."
        
        response = model.generate_content(prompt)
        
        return jsonify({"hasil": response.text})
    except Exception as e:
        # Menampilkan detail error dari Google
        return jsonify({"error": str(e)}), 500

