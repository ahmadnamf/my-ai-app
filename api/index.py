from flask import Flask, request, jsonify
# ... import lainnya ...

app = Flask(__name__) # Baris ini wajib ada

@app.route("/api/generate", methods=["POST"])
def generate():
    # ... isi fungsi Anda ...
    return jsonify({"hasil": "tes"})
