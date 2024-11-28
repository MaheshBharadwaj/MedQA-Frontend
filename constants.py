import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-api-key")
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", 5))

CHAT_TITLE_PROMPT = f"""Based on the following patient information and medical query, generate a concise, one-line title (max 50 characters) that captures the key concern or topic. 
    Format: Keep it in the format 'Patient Topic - Concern'

    Patient Information:"""