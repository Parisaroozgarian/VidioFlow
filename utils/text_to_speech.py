import os
import io
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

VALID_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def generate_speech(text, voice="alloy"):
    """
    Generate speech from text using OpenAI's TTS API.

    Args:
        text (str): The text to convert to speech.
        voice (str): alloy | echo | fable | onyx | nova | shimmer

    Returns:
        io.BytesIO: Buffer containing MP3 audio data.
    """
    # OpenAI TTS limit is 4096 characters
    if len(text) > 4096:
        text = text[:4093] + "..."

    if voice not in VALID_VOICES:
        voice = "alloy"

    client = _get_client()

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        buffer = io.BytesIO()
        # response.content holds the full audio bytes in the current SDK
        buffer.write(response.content)
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise Exception(f"Error generating speech: {str(e)}")


def extract_speech_sections(script, max_length=4000):
    """
    Break a long script into TTS-friendly sections, stripping stage directions.

    Returns:
        list[str]: Clean text sections each under max_length characters.
    """
    lines = script.split('\n')
    sections = []
    current_section = ""

    for line in lines:
        # Strip visual/caption stage directions
        if "[VISUAL" in line or "[CAPTION" in line:
            continue
        # Skip section headers
        if re.match(r'^[A-Z\s]+:', line) or line.startswith('#'):
            if current_section.strip():
                sections.append(current_section.strip())
            current_section = ""
            continue

        if len(current_section) + len(line) + 1 > max_length:
            if current_section.strip():
                sections.append(current_section.strip())
            current_section = line
        else:
            current_section = (current_section + " " + line).strip()

    if current_section.strip():
        sections.append(current_section.strip())

    return sections
