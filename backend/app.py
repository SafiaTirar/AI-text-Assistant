import os
import tempfile

from flask import Flask, request, jsonify, send_file, render_template, after_this_request
from dotenv import load_dotenv

from llm_client import call_llm
from processors import build_prompt
from pdf_generator import generate_pdf

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/process", methods=["POST"])
def process_text():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Le corps de la requête doit être un objet JSON"}), 400

    text = data.get("text", "")
    operation = data.get("operation", "resume_court")
    language = data.get("language", "auto")
    options = data.get("options", {})

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Aucun texte fourni"}), 400
    if not isinstance(options, dict):
        return jsonify({"error": "Le champ options doit être un objet JSON"}), 400

    prompt = build_prompt(text, operation, language, options)
    result = call_llm(prompt)
    if isinstance(result, str) and result.startswith("[Erreur LLM Groq]"):
        return jsonify({"error": result}), 502
    detected_lang = "ar" if any("\u0600" <= char <= "\u06ff" for char in result) else "fr"

    return jsonify({
        "result": result,
        "detected_language": detected_lang
    })


@app.route("/api/download-pdf", methods=["POST"])
def download_pdf():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Le corps de la requête doit être un objet JSON"}), 400

    content = data.get("content", "Aucun contenu")
    if not isinstance(content, str):
        return jsonify({"error": "Le contenu doit être une chaîne de caractères"}), 400

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_path = temp.name
    temp.close()
    generate_pdf(content, temp_path)

    @after_this_request
    def remove_temp_file(response):
        try:
            os.remove(temp_path)
        except OSError:
            pass
        return response

    return send_file(
        temp_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="resultat.pdf"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)
