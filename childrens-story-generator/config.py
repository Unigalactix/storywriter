import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings for the children's story generator application

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))

# AutoGen Configuration
LLM_CONFIG = {
    "model": MODEL_NAME,
    "api_key": OPENAI_API_KEY,
    "temperature": TEMPERATURE,
    "max_tokens": MAX_TOKENS,
}

# Story Configuration
GENRES = [
    "Fantasy",
    "Adventure", 
    "Fairy Tale",
    "Science Fiction",
    "Mystery",
    "Animal Story",
    "Friendship",
    "Educational"
]

DEFAULT_GENRE = "Fantasy"
DEFAULT_TITLE = "A Magical Adventure"