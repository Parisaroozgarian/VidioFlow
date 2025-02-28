import os
import io
import re
import base64
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_speech(text, voice="alloy"):
    """
    Generate speech from text using OpenAI's TTS API.
    
    Args:
        text (str): The text to convert to speech
        voice (str): The voice to use (options: alloy, echo, fable, onyx, nova, shimmer)
        
    Returns:
        io.BytesIO: A buffer containing the audio data
    """
    # Limit text to 4096 characters (OpenAI's limitation)
    if len(text) > 4096:
        text = text[:4093] + "..."
    
    api_key = os.getenv("OPENAI_API_KEY", "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")
    if not api_key:
        raise ValueError("OpenAI API key is not set")
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=api_key)
    
    # Validate voice option
    valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if voice not in valid_voices:
        voice = "alloy"  # Default to alloy if invalid voice
    
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        # Create a buffer to store the audio data
        buffer = io.BytesIO()
        for chunk in response.iter_bytes(chunk_size=4096):
            buffer.write(chunk)
        
        buffer.seek(0)
        return buffer
    except Exception as e:
        raise Exception(f"Error generating speech: {str(e)}")

def extract_speech_sections(script, max_length=4000):
    """
    Extract sections from a script for text-to-speech conversion.
    Breaks down long scripts into smaller sections.
    
    Args:
        script (str): The full script
        max_length (int): Maximum length of each section
        
    Returns:
        list: List of script sections
    """
    # Split script by line breaks
    lines = script.split('\n')
    
    sections = []
    current_section = ""
    
    for line in lines:
        # Skip visual notes and other non-speech content
        if "[VISUAL" in line or "[CAPTION" in line:
            continue
            
        # Skip section headers (lines with all caps and colon)
        if re.match(r'^[A-Z\s]+:', line) or line.startswith('#'):
            if current_section:
                sections.append(current_section)
                current_section = ""
            continue
        
        # Add line to current section
        if len(current_section + line) > max_length:
            sections.append(current_section)
            current_section = line
        else:
            if current_section:
                current_section += " " + line
            else:
                current_section = line
    
    # Add the last section
    if current_section:
        sections.append(current_section)
    
    return sections

# Example usage
if __name__ == "__main__":
    try:
        # Test with a short text
        test_text = "Welcome to VidioFlow, the ultimate video script generator. This is a test of the text-to-speech functionality."
        audio_buffer = generate_speech(test_text)
        
        # Save to a file for testing
        with open("test_speech.mp3", "wb") as f:
            f.write(audio_buffer.read())
            
        print("Speech generated successfully!")
    except Exception as e:
        print(f"Error: {e}")