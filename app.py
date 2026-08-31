"""
PROJECT: Omni-Portal Professional (Academic, Computational & Media Mega-Platform)
ROLE: Enterprise Full-Stack Python Architect
SYSTEMS: Flask API, Tailwind Front-End, Educational Tools, Converters & Multi-lingual Engines
"""

import os
import io
import math
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import PyPDF2
from docx import Document
import openpyxl

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit

# --- SUBSYSTEM 1: PALETTE & SYSTEM DATA ---
COLOR_PALETTES = [
    ["#0f172a", "#1e293b", "#334155", "#38bdf8", "#f8fafc"],
    ["#022c22", "#064e3b", "#047857", "#10b981", "#ecfdf5"],
    ["#31103f", "#581c87", "#7e22ce", "#a855f7", "#faf5ff"],
    ["#1c1917", "#44403c", "#78716c", "#f97316", "#fff7ed"]
]

DAILY_ARTICLES = [
    {
        "title": "CSS/PMS Strategy: Structural Analysis of Essay Writing",
        "category": "Competitive Exams",
        "content": "A high-scoring CSS/PMS essay relies on a robust thesis statement, coherent topic sentences, and empirical evidence from international relations or socio-economic indicators."
    },
    {
        "title": "Modern Systems Programming: Memory Management in C/C++ vs Python",
        "category": "Computer Science",
        "content": "Understanding stack vs. heap allocation is crucial for building high-throughput systems. While Python relies on automatic reference counting and GC, C requires manual allocation."
    }
]

# --- SUBSYSTEM 3: 5-LANGUAGE LEXICON ---
LEXICON_DB = {
    "education": {
        "pos": "Noun",
        "en_us": "Education",
        "ur_pk": "تعلیم (Taleem)",
        "ur_in": "शिक्षा (Shiksha)",
        "ps_kpk": "زدکړه (Zadkra)",
        "zh": "教育 (Jiàoyù)"
    },
    "governance": {
        "pos": "Noun",
        "en_us": "Governance",
        "ur_pk": "حکمرانی (Hukmrani)",
        "ur_in": "शासन (Shasan)",
        "ps_kpk": "حکومتولي (Hukumatwali)",
        "zh": "治理 (Zhìlǐ)"
    }
}

# --- ROUTES ---

@app.route('/')
def home():
    palette = random.choice(COLOR_PALETTES)
    article = random.choice(DAILY_ARTICLES)
    return render_template('index.html', palette=palette, article=article)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    # 4-Day Weather Forecast (Peshawar Default / Mock Engine)
    forecast = [
        {"day": "Today", "temp": "34°C", "condition": "Sunny", "location": "Peshawar"},
        {"day": "Tomorrow", "temp": "32°C", "condition": "Partly Cloudy", "location": "Peshawar"},
        {"day": "Day 3", "temp": "30°C", "condition": "Rain Shower", "location": "Peshawar"},
        {"day": "Day 4", "temp": "33°C", "condition": "Clear Sky", "location": "Peshawar"}
    ]
    return jsonify({"status": "success", "data": forecast})

@app.route('/api/calculate', methods=['POST'])
def scientific_calculator():
    data = request.json or {}
    expr = data.get('expression', '')
    try:
        # Safe evaluation context for physics & math
        allowed_names = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
            "log": math.log, "pow": math.pow
        }
        result = eval(expr, {"__builtins__": None}, allowed_names)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": "Invalid Expression"}), 400

@app.route('/api/lexicon/<word>', methods=['GET'])
def lookup_lexicon(word):
    entry = LEXICON_DB.get(word.lower())
    if entry:
        return jsonify({"status": "success", "data": entry})
    return jsonify({"status": "error", "message": "Word not found in 5-language database"}), 404

@app.route('/api/convert/image-to-pdf', methods=['POST'])
def convert_image_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    try:
        image = Image.open(file.stream)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        pdf_bytes = io.BytesIO()
        image.save(pdf_bytes, format='PDF')
        pdf_bytes.seek(0)
        
        return send_file(
            pdf_bytes,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='converted_document.pdf'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/typing/evaluate', methods=['POST'])
def evaluate_typing():
    data = request.json or {}
    original = data.get('original', '')
    typed = data.get('typed', '')
    time_seconds = float(data.get('time_seconds', 1))

    typed_words = typed.strip().split()
    orig_words = original.strip().split()
    
    correct_words = sum(1 for tw, ow in zip(typed_words, orig_words) if tw == ow)
    wpm = (len(typed_words) / time_seconds) * 60
    accuracy = (correct_words / max(len(orig_words), 1)) * 100

    return jsonify({
        "gross_wpm": round(wpm, 2),
        "accuracy": f"{round(accuracy, 1)}%",
        "net_speed": round(wpm * (accuracy / 100), 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
