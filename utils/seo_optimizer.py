import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def optimize_content(content, keywords=""):
    client = _get_client()

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
6. Enhance content hierarchy with proper H1, H2, H3 structure
7. Improve content flow and readability

Original content:
{content}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
    client = _get_client()

    keywords_instruction = ""
    if keywords:
        keywords_list = [k.strip() for k in keywords.split(',')]
        keywords_instruction = f"Target keywords to check for: {', '.join(keywords_list)}"

    prompt = f"""
Analyze the following content for SEO effectiveness and return a JSON object with EXACTLY these keys:

- score              (integer 0-100)
- keyword_analysis   (string)
- structure_analysis (string)
- readability_score  (integer 0-100)
- recommendations    (list of 3-5 short actionable strings)

{keywords_instruction}

Content to analyze:
{content}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert SEO analyzer. Always respond with valid JSON matching the exact keys requested."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Error analyzing SEO: {str(e)}")


def generate_meta_tags(content, title="", keywords=""):
    client = _get_client()
    context = content[:1000] + "..." if len(content) > 1000 else content

    prompt = f"""
Generate optimized SEO meta tags for the following content.

Title: {title}
Keywords: {keywords}

Content excerpt:
{context}

Return a JSON object with:
- title_tag        : SEO-optimized title (max 60 characters)
- meta_description : meta description (max 155 characters)
- focus_keyword    : single suggested focus keyword
- secondary_keywords: list of 5-7 secondary keywords
- url_slug         : optimized URL slug
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
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Error generating meta tags: {str(e)}")
