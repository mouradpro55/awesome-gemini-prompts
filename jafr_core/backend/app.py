from flask import Flask, render_template, request, jsonify
from backend.nlp import clean_and_normalize
from backend.engine import macro_value, digital_root, bast_extended_value
from backend.elements import calculate_elements
from backend.quran_db import search_quran, is_db_empty, ingest_quran
import os

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    text = data.get('text', '')
    rule = data.get('rule', 'east')
    unify_hamzat = data.get('unify_hamzat', True)
    expand_shaddah = data.get('expand_shaddah', False)

    clean_text = clean_and_normalize(text, unify_hamzat, expand_shaddah)
    macro = macro_value(clean_text, rule)
    saghir = digital_root(macro)
    bast = bast_extended_value(clean_text, rule)

    return jsonify({
        'macro': macro,
        'saghir': saghir,
        'bast': bast
    })

@app.route('/api/elements', methods=['POST'])
def elements():
    data = request.json
    text = data.get('text', '')
    clean_text = clean_and_normalize(text, True, False)
    counts, dominant = calculate_elements(clean_text)

    total = sum(counts.values())
    percentages = {k: (v / total * 100) if total > 0 else 0 for k, v in counts.items()}

    return jsonify({
        'counts': counts,
        'percentages': percentages,
        'dominant': dominant
    })

@app.route('/api/search_quran', methods=['POST'])
def search_quran_api():
    data = request.json
    val = data.get('value')
    rule = data.get('rule', 'east')

    try:
        val = int(val)
    except (ValueError, TypeError):
        return jsonify({'results': []})

    results = search_quran(val, rule)
    return jsonify({'results': results})

def init_app():
    if is_db_empty():
        print("Initializing database...")
        ingest_quran()

if __name__ == '__main__':
    init_app()
    app.run(debug=True, port=5000)
