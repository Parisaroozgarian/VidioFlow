from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime
from dotenv import load_dotenv
from utils.script_generator import (
    generate_video_script,
    analyze_script_content,
    generate_b_roll_suggestions,
    generate_thumbnail_suggestions,
    get_available_templates
)
from utils.seo_optimizer import optimize_content, analyze_seo_score
from utils.export import generate_pdf, generate_docx
from utils.text_to_speech import generate_speech

load_dotenv()

app = Flask(__name__)

# NOTE: script_versions is stored in memory.
# On Vercel (serverless) each cold start resets this dict.
# For persistent versioning, replace with a database (e.g. Vercel KV / Postgres).
script_versions = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/templates', methods=['GET'])
def get_templates():
    try:
        return jsonify(get_available_templates())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-script', methods=['POST'])
def script_endpoint():
    data = request.json
    topic = data.get('topic', '')
    duration = data.get('duration', 5)
    tone = data.get('tone', 'informative')
    target_audience = data.get('targetAudience', 'general')
    template_id = data.get('templateId', None)
    language = data.get('language', 'english')

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    try:
        script = generate_video_script(
            topic=topic,
            duration=duration,
            tone=tone,
            target_audience=target_audience,
            template_id=template_id,
            language=language
        )

        if data.get('optimizeForSEO', False):
            keywords = data.get('keywords', '')
            script = optimize_content(script, keywords)

        script_id = datetime.now().strftime('%Y%m%d%H%M%S')

        if topic not in script_versions:
            script_versions[topic] = []

        script_versions[topic].append({
            "id": script_id,
            "script": script,
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "topic": topic,
                "duration": duration,
                "tone": tone,
                "target_audience": target_audience,
                "template_id": template_id,
                "language": language
            }
        })

        return jsonify({"script": script, "script_id": script_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/analyze-script', methods=['POST'])
def analyze_script_endpoint():
    data = request.json
    script = data.get('script', '')
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    try:
        return jsonify(analyze_script_content(script))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-b-roll', methods=['POST'])
def b_roll_endpoint():
    data = request.json
    script = data.get('script', '')
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    try:
        return jsonify(generate_b_roll_suggestions(script))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-thumbnails', methods=['POST'])
def thumbnails_endpoint():
    data = request.json
    topic = data.get('topic', '')
    script = data.get('script', '')
    if not topic or not script:
        return jsonify({"error": "Both topic and script are required"}), 400
    try:
        return jsonify(generate_thumbnail_suggestions(topic, script))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/optimize-seo', methods=['POST'])
def optimize_endpoint():
    data = request.json
    content = data.get('content', '')
    if not content:
        return jsonify({"error": "Content is required"}), 400
    try:
        return jsonify({"optimized_content": optimize_content(content, data.get('keywords', ''))})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/seo-analysis', methods=['POST'])
def seo_analysis_endpoint():
    data = request.json
    content = data.get('content', '')
    if not content:
        return jsonify({"error": "Content is required"}), 400
    try:
        return jsonify(analyze_seo_score(content, data.get('keywords', '')))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/script-versions', methods=['GET'])
def get_script_versions():
    topic = request.args.get('topic', '')
    if not topic or topic not in script_versions:
        return jsonify({"versions": []})
    try:
        versions = [{
            "id": v["id"],
            "timestamp": v["timestamp"],
            "parameters": v["parameters"]
        } for v in script_versions[topic]]
        return jsonify({"versions": versions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/script-version/<script_id>', methods=['GET'])
def get_script_version(script_id):
    for topic in script_versions:
        for version in script_versions[topic]:
            if version["id"] == script_id:
                return jsonify(version)
    return jsonify({"error": "Script version not found"}), 404


@app.route('/export-pdf', methods=['POST'])
def export_pdf_endpoint():
    data = request.json
    script = data.get('script', '')
    title = data.get('title', 'Video Script')
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    try:
        pdf_bytes = generate_pdf(script, title)
        return jsonify({
            "success": True,
            "file_data": base64.b64encode(pdf_bytes.getvalue()).decode('utf-8'),
            "filename": f"{title.replace(' ', '_')}.pdf"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/export-docx', methods=['POST'])
def export_docx_endpoint():
    data = request.json
    script = data.get('script', '')
    title = data.get('title', 'Video Script')
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    try:
        docx_bytes = generate_docx(script, title)
        return jsonify({
            "success": True,
            "file_data": base64.b64encode(docx_bytes.getvalue()).decode('utf-8'),
            "filename": f"{title.replace(' ', '_')}.docx"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-speech', methods=['POST'])
def speech_endpoint():
    data = request.json
    text = data.get('text', '')
    voice = data.get('voice', 'alloy')
    if not text:
        return jsonify({"error": "Text content is required"}), 400
    try:
        audio_data = generate_speech(text, voice)
        return jsonify({
            "success": True,
            "audio_data": base64.b64encode(audio_data.getvalue()).decode('utf-8')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
# Flask app
