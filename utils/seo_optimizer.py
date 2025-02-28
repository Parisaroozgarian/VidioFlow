import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def optimize_content(content, keywords=""):
    """
    Optimize content for SEO using OpenAI's API.
    
    Args:
        content (str): The content to optimize.
        keywords (str): Target keywords to include, comma-separated.
        
    Returns:
        str: SEO-optimized content.
    """
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    # Prepare keywords for the prompt
    keywords_instruction = ""
    if keywords:
        keywords_list = [k.strip() for k in keywords.split(',')]
        keywords_instruction = f"Target keywords to incorporate naturally: {', '.join(keywords_list)}"
    
    prompt = f"""
    Please optimize the following content for SEO while maintaining its original message and tone.
    
    {keywords_instruction}
    
    Guidelines:
    1. Improve headings and subheadings for better clarity and keyword inclusion
    2. Optimize sentence structure and paragraph length for readability
    3. Naturally incorporate keywords without keyword stuffing
    4. Ensure proper semantic structure (intro, body, conclusion)
    5. Add appropriate calls-to-action where relevant
    6. Improve meta description if one is provided
    7. Enhance content hierarchy with proper H1, H2, H3 structure
    8. Improve content flow and readability
    
    Original content:
    {content}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" for better results if available
            messages=[
                {"role": "system", "content": "You are an expert SEO content optimizer with deep knowledge of search engine algorithms and content optimization strategies."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error optimizing content: {str(e)}")

def analyze_seo_score(content, keywords=""):
    """
    Analyze content and provide an SEO score and recommendations.
    
    Args:
        content (str): The content to analyze.
        keywords (str): Target keywords to check for, comma-separated.
        
    Returns:
        dict: Dictionary containing score and recommendations.
    """
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    keywords_instruction = ""
    if keywords:
        keywords_list = [k.strip() for k in keywords.split(',')]
        keywords_instruction = f"Target keywords to check for: {', '.join(keywords_list)}"
    
    prompt = f"""
    Analyze the following content for SEO effectiveness and provide:
    1. An overall SEO score from 0-100
    2. Detailed keyword analysis (usage, density, placement)
    3. Content structure assessment (headings, paragraphs, flow)
    4. Readability score from 0-100
    5. Specific recommendations for improvement (at least 3-5 actionable tips)
    
    {keywords_instruction}
    
    Content to analyze:
    {content}
    
    Format your response as JSON with the following structure:
    {{
        "score": 85,
        "keyword_analysis": "Analysis of keyword usage",
        "structure_analysis": "Analysis of content structure",
        "readability_score": 75,
        "recommendations": ["Rec 1", "Rec 2", "Rec 3"]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" for better results if available
            messages=[
                {"role": "system", "content": "You are an expert SEO analyzer with deep knowledge of search engine algorithms, content optimization, and web analytics. Provide detailed, actionable analysis in JSON format."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise Exception(f"Error analyzing SEO: {str(e)}")

def generate_meta_tags(content, title="", keywords=""):
    """
    Generate SEO meta tags from content.
    
    Args:
        content (str): The content to analyze.
        title (str): The page title.
        keywords (str): Target keywords to include.
        
    Returns:
        dict: Dictionary containing meta tags.
    """
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    # Extract first 1000 characters for context if content is long
    context = content[:1000] + "..." if len(content) > 1000 else content
    
    prompt = f"""
    Generate optimized SEO meta tags for the following content:
    
    Title: {title}
    Keywords: {keywords}
    
    Content excerpt:
    {context}
    
    Please create:
    1. An SEO-optimized title tag (max 60 characters)
    2. A meta description (max 155 characters) that includes key benefits and a call to action
    3. Suggested focus keyword
    4. 5-7 secondary keywords/phrases based on the content
    5. An optimized URL slug
    
    Format your response as JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in SEO and meta tag optimization."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise Exception(f"Error generating meta tags: {str(e)}")

# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        sample_content = """
        Meditation for Beginners
        
        Meditation is a practice that can help reduce stress and improve focus. Many people find it difficult to start meditating regularly. This guide will help you begin your meditation journey.
        
        First, find a quiet place to sit. Set a timer for 5 minutes. Close your eyes and focus on your breath. When your mind wanders, gently bring your attention back to your breathing.
        
        Try to practice daily for the best results. Over time, you can increase your meditation sessions to 10 or 15 minutes.
        
        Benefits of regular meditation include reduced anxiety, better sleep, and improved concentration. Many beginners notice positive changes within just a few weeks of consistent practice.
        """
        
        optimized = optimize_content(sample_content, "meditation, beginners, stress reduction, mindfulness")
        print("Optimized Content:")
        print(optimized)
        
        analysis = analyze_seo_score(sample_content, "meditation, beginners, stress reduction")
        print("\nSEO Analysis:")
        print(json.dumps(analysis, indent=2))
        
        meta_tags = generate_meta_tags(sample_content, "Meditation Guide", "meditation, beginners")
        print("\nMeta Tags:")
        print(json.dumps(meta_tags, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")