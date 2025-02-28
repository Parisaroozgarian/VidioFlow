from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import io
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

# Load environment variables
load_dotenv()


app = Flask(__name__)

# In-memory storage for script versions
# In a production app, you'd use a database
script_versions = {}

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available script templates."""
    try:
        templates = get_available_templates()
        return jsonify(templates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-script', methods=['POST'])
def script_endpoint():
    """Generate a video script based on the provided topic and parameters."""
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
        
        # If SEO optimization is requested
        if data.get('optimizeForSEO', False):
            keywords = data.get('keywords', '')
            script = optimize_content(script, keywords)
        
        # Generate a unique ID for this script
        script_id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Store the script version
        if not topic in script_versions:
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
            
        return jsonify({
            "script": script,
            "script_id": script_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze-script', methods=['POST'])
def analyze_script_endpoint():
    """Analyze a script and provide content metrics."""
    data = request.json
    script = data.get('script', '')
    
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    
    try:
        analytics = analyze_script_content(script)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-b-roll', methods=['POST'])
def b_roll_endpoint():
    """Generate B-roll suggestions for a script."""
    data = request.json
    script = data.get('script', '')
    
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    
    try:
        suggestions = generate_b_roll_suggestions(script)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-thumbnails', methods=['POST'])
def thumbnails_endpoint():
    """Generate thumbnail suggestions for a video."""
    data = request.json
    topic = data.get('topic', '')
    script = data.get('script', '')
    
    if not topic or not script:
        return jsonify({"error": "Both topic and script are required"}), 400
    
    try:
        suggestions = generate_thumbnail_suggestions(topic, script)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/optimize-seo', methods=['POST'])
def optimize_endpoint():
    """Optimize existing content for SEO."""
    data = request.json
    content = data.get('content', '')
    keywords = data.get('keywords', '')
    
    if not content:
        return jsonify({"error": "Content is required"}), 400
    
    try:
        optimized_content = optimize_content(content, keywords)
        return jsonify({"optimized_content": optimized_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/seo-analysis', methods=['POST'])
def seo_analysis_endpoint():
    """Analyze content for SEO effectiveness."""
    data = request.json
    content = data.get('content', '')
    keywords = data.get('keywords', '')
    
    if not content:
        return jsonify({"error": "Content is required"}), 400
    
    try:
        analysis = analyze_seo_score(content, keywords)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/script-versions', methods=['GET'])
def get_script_versions():
    """Get all versions of scripts for a particular topic."""
    topic = request.args.get('topic', '')
    
    if not topic or topic not in script_versions:
        return jsonify({"versions": []})
    
    try:
        # Return just the metadata, not the full scripts
        versions = [{
            "id": version["id"],
            "timestamp": version["timestamp"],
            "parameters": version["parameters"]
        } for version in script_versions[topic]]
        
        return jsonify({"versions": versions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/script-version/<script_id>', methods=['GET'])
def get_script_version(script_id):
    """Get a specific version of a script by ID."""
    for topic in script_versions:
        for version in script_versions[topic]:
            if version["id"] == script_id:
                return jsonify(version)
    
    return jsonify({"error": "Script version not found"}), 404

@app.route('/export-pdf', methods=['POST'])
def export_pdf_endpoint():
    """Export script as PDF."""
    data = request.json
    script = data.get('script', '')
    title = data.get('title', 'Video Script')
    
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    
    try:
        pdf_bytes = generate_pdf(script, title)
        
        # Convert bytes to base64 for frontend download
        pdf_base64 = base64.b64encode(pdf_bytes.getvalue()).decode('utf-8')
        
        return jsonify({
            "success": True,
            "file_data": pdf_base64,
            "filename": f"{title.replace(' ', '_')}.pdf"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/export-docx', methods=['POST'])
def export_docx_endpoint():
    """Export script as DOCX."""
    data = request.json
    script = data.get('script', '')
    title = data.get('title', 'Video Script')
    
    if not script:
        return jsonify({"error": "Script content is required"}), 400
    
    try:
        docx_bytes = generate_docx(script, title)
        
        # Convert bytes to base64 for frontend download
        docx_base64 = base64.b64encode(docx_bytes.getvalue()).decode('utf-8')
        
        return jsonify({
            "success": True,
            "file_data": docx_base64,
            "filename": f"{title.replace(' ', '_')}.docx"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-speech', methods=['POST'])
def speech_endpoint():
    """Generate speech from script text."""
    data = request.json
    text = data.get('text', '')
    voice = data.get('voice', 'default')
    
    if not text:
        return jsonify({"error": "Text content is required"}), 400
    
    try:
        audio_data = generate_speech(text, voice)
        
        # Convert bytes to base64 for frontend playback
        audio_base64 = base64.b64encode(audio_data.getvalue()).decode('utf-8')
        
        return jsonify({
            "success": True,
            "audio_data": audio_base64
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)