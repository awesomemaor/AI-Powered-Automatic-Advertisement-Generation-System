import os
from google import genai
from google.genai import types

# Load Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
print("GEMINI_API_KEY:", GEMINI_API_KEY)

def enhance_prompt_with_gemini(user_input: str):
    # check if key available
    if not GEMINI_API_KEY:
        print("Warning: GOOGLE_API_KEY not found in environment variables. Using original prompt.")
        return user_input

    try:
        # Initialize Gemini client
        client = genai.Client(api_key=GEMINI_API_KEY)
       
        system_instruction = """
        You are an expert AI Video Prompt Engineer.
        Rewrite the user's input into a highly detailed, cinematic prompt for an AI video generator.
        
        Guidelines:
        1. Focus on visual details: lighting, camera angles, texture, atmosphere.
        2. Keep it under 60 words.
        3. Do NOT add dialogue or script. purely visual description.
        4. Output ONLY the enhanced prompt.
        """
        
        # Call Gemini model to enhance the prompt
        response = client.models.generate_content(
            model='models/gemini-2.0-flash-lite-preview-02-05', 
            contents=f"{system_instruction}\n\nUser Input: {user_input}\nEnhanced Prompt:"
        )
        
        enhanced_text = response.text.strip()
        print(f"✨ Gemini Enhanced: {enhanced_text}")
        return enhanced_text

    except Exception as e:
        print(f"Gemini Error: {e}")
        return user_input