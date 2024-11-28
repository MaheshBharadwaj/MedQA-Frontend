import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your-api-key")
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", 5))
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "openid"]
REDIRECT_URI = "http://localhost:8501"
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.01:5000")
LOGIN_URL = os.getenv("LOGIN_URL", "http://127.0.0.1:5000/auth/login")

CHAT_TITLE_PROMPT = f"""Based on the following patient information and medical query, generate a concise, one-line title (max 50 characters) that captures the key concern or topic. 
    Format: Keep it in the format 'Patient Topic - Concern'

    Patient Information:"""