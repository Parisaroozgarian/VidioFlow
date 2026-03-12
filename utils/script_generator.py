import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SCRIPT_TEMPLATES = {
    "tutorial": {
        "name": "Tutorial / How-To",
        "structure": [
            {"section": "Introduction", "desc": "Introduce yourself and the topic, explain why it matters"},
            {"section": "Problem Statement", "desc": "Clearly state the problem or need this tutorial addresses"},
            {"section": "Materials/Prerequisites", "desc": "List what viewers will need to follow along"},
            {"section": "Step-by-Step Instructions", "desc": "Break down the process into clear steps"},
            {"section": "Common Issues/FAQs", "desc": "Address potential problems viewers might encounter"},
            {"section": "Conclusion", "desc": "Summarize what was learned and suggest next steps"}
        ]
    },
    "review": {
        "name": "Product/Service Review",
        "structure": [
            {"section": "Introduction", "desc": "Introduce the product/service and your experience with it"},
            {"section": "Overview", "desc": "Provide general information about the product/service"},
            {"section": "Key Features", "desc": "Highlight the most important features"},
            {"section": "Pros and Cons", "desc": "Balanced analysis of strengths and weaknesses"},
            {"section": "Comparison", "desc": "Compare with alternatives if applicable"},
            {"section": "Recommendation", "desc": "Final verdict and who should buy/use it"}
        ]
    },
    "explainer": {
        "name": "Explainer / Educational",
        "structure": [
            {"section": "Hook", "desc": "Capture interest with an intriguing fact or question"},
            {"section": "Introduction", "desc": "Introduce the topic and why it's important"},
            {"section": "Main Concepts", "desc": "Explain key ideas in simple, accessible terms"},
            {"section": "Examples", "desc": "Provide real-world examples or case studies"},
            {"section": "Deeper Insights", "desc": "Explore nuances or advanced aspects of the topic"},
            {"section": "Practical Applications", "desc": "How viewers can apply this knowledge"},
            {"section": "Conclusion", "desc": "Summarize key takeaways"}
        ]
    },
    "storytelling": {
        "name": "Storytelling / Narrative",
        "structure": [
            {"section": "Hook", "desc": "Capture attention with an intriguing opening"},
            {"section": "Setup", "desc": "Establish the context, characters, or situation"},
            {"section": "Conflict/Challenge", "desc": "Introduce the main problem or obstacle"},
            {"section": "Rising Action", "desc": "Show how the situation develops or intensifies"},
            {"section": "Climax", "desc": "Present the turning point or key realization"},
            {"section": "Resolution", "desc": "Show how the situation is resolved"},
            {"section": "Takeaway", "desc": "Share the lesson or meaning of the story"}
        ]
    },
    "vlog": {
        "name": "Vlog / Day-in-the-Life",
        "structure": [
            {"section": "Intro", "desc": "Greet viewers and set expectations for the video"},
            {"section": "Morning Routine", "desc": "Show how the day starts"},
            {"section": "Main Activities", "desc": "Highlight key activities or events of the day"},
            {"section": "Challenges", "desc": "Share any obstacles or interesting moments"},
            {"section": "Reflections", "desc": "Personal thoughts about the day's experiences"},
            {"section": "Conclusion", "desc": "Wrap up and preview what's coming next"}
        ]
    }
}


def _get_client():
    """Return an OpenAI client, raising clearly if the key is missing."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def _extract_list(data: dict) -> list:
    """
    OpenAI json_object mode always returns an object, never a bare array.
    This helper finds and returns the first list value in the response dict.
    Falls back to wrapping the whole dict in a list if no list is found.
    """
    for value in data.values():
        if isinstance(value, list):
            return value
    return [data]


def get_available_templates():
    return {tid: t["name"] for tid, t in SCRIPT_TEMPLATES.items()}


def generate_video_script(topic, duration=5, tone="informative",
                          target_audience="general", template_id=None,
                          language="english"):
    client = _get_client()
    word_count = duration * 150

    prompt = f"""
Create a video script about '{topic}' in {language}.

Target audience: {target_audience}
Tone: {tone}
Target length: Approximately {word_count} words ({duration} minutes)
"""

    if template_id and template_id in SCRIPT_TEMPLATES:
        template = SCRIPT_TEMPLATES[template_id]
        prompt += f"\nTemplate: {template['name']}\n\nStructure:"
        for section in template["structure"]:
            prompt += f"\n- {section['section']}: {section['desc']}"
    else:
        prompt += """
The script should include:
1. An engaging introduction that hooks the viewer
2. Main content sections with key points about the topic
3. A clear and concise conclusion with a call to action
"""

    prompt += """

Format the script with clear SECTION HEADINGS.
For each section, include:
1. The main script content (what the presenter will say)
2. [VISUAL NOTES] with specific B-roll and visual suggestions
3. [CAPTION] suggestions for important text overlays

At the end, provide 3 thumbnail suggestions with descriptions.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert video script writer who creates highly engaging, well-structured scripts with detailed visual guidance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating script: {str(e)}")


def generate_b_roll_suggestions(script, num_suggestions=5):
    client = _get_client()

    prompt = f"""
Based on the following video script, suggest {num_suggestions} specific B-roll shots that would enhance the video.

For each suggestion provide:
1. description: A detailed description of the shot
2. timing: When in the script it should appear
3. purpose: What purpose it serves (illustrative, emotional, transitional, etc.)

Script:
{script}

Return a JSON object with a single key "suggestions" whose value is a list of objects,
each with the keys: description, timing, purpose.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert video producer with deep knowledge of visual storytelling."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return _extract_list(data)
    except Exception as e:
        raise Exception(f"Error generating B-roll suggestions: {str(e)}")


def analyze_script_content(script):
    client = _get_client()

    prompt = f"""
Analyze the following video script and return a JSON object with EXACTLY these keys:

- readability_score  (integer 1-100)
- reading_pace       (integer, words per minute)
- tone_analysis      (string description)
- complexity_level   (one of: beginner / intermediate / advanced)
- word_count         (integer)
- estimated_duration (string, e.g. "3 minutes 20 seconds")
- key_strength       (string, one sentence)
- top_suggestion     (string, one sentence improvement tip)

Script:
{script}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content analyst specializing in video scripts. Always respond with valid JSON matching the exact keys requested."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Error analyzing script: {str(e)}")


def generate_thumbnail_suggestions(topic, script):
    client = _get_client()
    script_excerpt = script[:500] + "..." if len(script) > 500 else script

    prompt = f"""
Suggest 3 compelling thumbnail ideas for a YouTube video on this topic: "{topic}"

Script excerpt:
{script_excerpt}

Return a JSON object with a single key "thumbnails" whose value is a list of 3 objects.
Each object must have these keys:
- title        : short name for the thumbnail concept
- description  : detailed visual description (composition, elements, colours)
- text_overlay : short impactful text for the thumbnail (max 6 words)
- appeal       : why this would attract viewers
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in YouTube video marketing and thumbnail design."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return _extract_list(data)
    except Exception as e:
        raise Exception(f"Error generating thumbnail suggestions: {str(e)}")
# Script generator
