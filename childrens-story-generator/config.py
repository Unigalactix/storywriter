import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings for the children's story generator application

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4000"))  # Increased for longer stories

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
    "max_messages": 25,  # Increased for longer collaboration
    "allow_repeated_speaker": True,
    "timeout": 600  # 10 minutes timeout for longer stories
}

# Story Configuration - Enhanced for 10+ page stories
STORY_CONFIG = {
    "target_pages": 10,
    "words_per_page": 150,  # Typical for children's books
    "min_total_words": 1500,  # 10 pages * 150 words
    "chapters": 5,  # Divide story into chapters
    "collaborative_rounds": 3  # Number of collaboration rounds between agents
}