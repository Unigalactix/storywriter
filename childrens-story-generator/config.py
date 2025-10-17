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

# Validate API key
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# AutoGen Configuration - Updated for new API
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

# Agent Configuration
AGENT_CONFIG = {
    "max_consecutive_auto_reply": 3,
    "human_input_mode": "NEVER",
    "code_execution_config": False
}

# Team Configuration
TEAM_CONFIG = {
    "max_messages": 15,
    "allow_repeated_speaker": True,
    "timeout": 300  # 5 minutes timeout
}