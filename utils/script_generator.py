import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define script templates
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

def get_available_templates():
    """Return a list of available script templates"""
    return {template_id: template["name"] for template_id, template in SCRIPT_TEMPLATES.items()}

def generate_video_script(topic, duration=5, tone="informative", target_audience="general", template_id=None, language="english"):
    """
    Generate a video script using OpenAI's API.
    
    Args:
        topic (str): The main topic of the video.
        duration (int): Approximate duration of the video in minutes.
        tone (str): The tone of the script (informative, entertaining, professional, etc.).
        target_audience (str): The target audience for the video.
        template_id (str): The ID of the template to use, if any.
        language (str): The language to generate the script in.
        
    Returns:
        str: The generated video script.
    """
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    # Calculate approximate word count based on duration
    # Average speaking rate is about 150 words per minute
    word_count = duration * 150
    
    # Base prompt
    prompt = f"""
    Create a video script about '{topic}' in {language}.
    
    Target audience: {target_audience}
    Tone: {tone}
    Target length: Approximately {word_count} words ({duration} minutes)
    """
    
    # Add template structure if specified
    if template_id and template_id in SCRIPT_TEMPLATES:
        template = SCRIPT_TEMPLATES[template_id]
        prompt += f"\nTemplate: {template['name']}\n\nStructure:"
        
        for section in template["structure"]:
            prompt += f"\n- {section['section']}: {section['desc']}"
            
    else:
        # Default structure if no template is specified
        prompt += """
        The script should include:
        1. An engaging introduction that hooks the viewer
        2. Main content sections with key points about the topic
        3. A clear and concise conclusion with a call to action
        """
    
    # Add formatting instructions
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
            model="gpt-3.5-turbo",  # Can use "gpt-4" for better results if available
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
    """
    Generate specific B-roll suggestions for a video script.
    
    Args:
        script (str): The video script.
        num_suggestions (int): Number of B-roll suggestions to generate.
        
    Returns:
        list: A list of B-roll suggestions.
    """
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    Based on the following video script, suggest {num_suggestions} specific B-roll shots that would enhance the video. 
    
    For each suggestion, provide:
    1. A detailed description of the shot
    2. When in the script it should appear
    3. What purpose it serves (illustrative, emotional, transitional, etc.)
    
    Script:
    {script}
    
    Format your response as a JSON list of objects with these properties:
    1. description: detailed description of the shot
    2. timing: when in the script to use it
    3. purpose: the purpose it serves
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
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise Exception(f"Error generating B-roll suggestions: {str(e)}")

def analyze_script_content(script):
    """
    Analyze the script content for readability, engagement, and other metrics.
    
    Args:
        script (str): The video script to analyze.
        
    Returns:
        dict: Analytics about the script.
    """
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    Analyze the following video script and provide detailed metrics. Your analysis should include:
    
    1. Overall readability score (on a scale of 1-100)
    2. Estimated reading/speaking pace (words per minute)
    3. Tone analysis (formal/informal, friendly/authoritative, etc.)
    4. Complexity level (beginner/intermediate/advanced)
    5. Engagement metrics (hooks, calls to action, emotional triggers)
    6. Word count and estimated duration
    7. Key strength of the script
    8. Top suggestion for improvement
    
    Script to analyze:
    {script}
    
    Format your response as a JSON object.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content analyst specializing in video scripts and engagement metrics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise Exception(f"Error analyzing script: {str(e)}")

def generate_thumbnail_suggestions(topic, script):
    """
    Generate thumbnail suggestions for a video based on its topic and script.
    
    Args:
        topic (str): The video topic
        script (str): The video script
        
    Returns:
        list: A list of thumbnail suggestions
    """
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    # Extract first 500 characters of script for context
    script_excerpt = script[:500] + "..." if len(script) > 500 else script
    
    prompt = f"""
    Suggest 3 compelling thumbnail ideas for a YouTube video on this topic: "{topic}"
    
    Script excerpt:
    {script_excerpt}
    
    For each thumbnail suggestion, provide:
    1. A detailed visual description (composition, elements, colors)
    2. Suggested text overlay (keep it short and impactful)
    3. Why this would attract clicks (psychological appeal)
    
    Format your response as a JSON list of objects with these properties:
    1. title: a short name for the thumbnail concept
    2. description: detailed visual description
    3. text_overlay: suggested text for the thumbnail
    4. appeal: why this would attract viewers
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
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise Exception(f"Error generating thumbnail suggestions: {str(e)}")

# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        example_script = generate_video_script(
            topic="The Benefits of Meditation",
            duration=3,
            tone="friendly",
            target_audience="beginners",
            template_id="tutorial"
        )
        print(example_script)
        
        # Test analytics
        analytics = analyze_script_content(example_script)
        print("\nScript Analytics:")
        print(json.dumps(analytics, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")