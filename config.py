import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────
GOOGLE_API_KEY  = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_CSE_ID   = os.getenv("GOOGLE_CSE_ID", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY", "")

# ── Settings ──────────────────────────────────────────
MAX_REVIEWS_PER_SOURCE = 5
GROQ_MODEL   = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-2.5-flash"