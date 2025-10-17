from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import LLM_CONFIG

class CharacterAgent:
    """Agent responsible for developing characters for children's stories"""
    
    def __init__(self):
        # Create model client
        self.model_client = OpenAIChatCompletionClient(
            model=LLM_CONFIG["model"],
            api_key=LLM_CONFIG["api_key"],
            temperature=LLM_CONFIG["temperature"],
            max_tokens=LLM_CONFIG["max_tokens"]
        )
        
        self.agent = AssistantAgent(
            name="Character_Developer",
            description="Creates detailed, engaging characters for multi-page children's stories with rich backgrounds and development arcs",
            model_client=self.model_client,
            system_message="""You are an expert character developer for children's stories. Your role is to create rich, multi-dimensional characters for 10+ page stories.

CORE RESPONSIBILITIES:
1. Create 3-5 main characters with detailed profiles
2. Develop character relationships and dynamics
3. Design character growth arcs throughout the story
4. Ensure diversity, inclusion, and positive role models
5. Create supporting characters when needed
6. Plan character development across story chapters

CHARACTER PROFILE REQUIREMENTS:
For each main character, provide:
- Full name and age (4-12 years old)
- Physical appearance (child-friendly description)
- Personality traits (3-5 key traits)
- Special abilities, talents, or interests
- Background/family situation
- Goals and motivations
- Character flaw/challenge to overcome
- How they grow throughout the story
- Relationships with other characters

STORY STRUCTURE SUPPORT:
- Design characters that can carry a 10-page narrative
- Create character conflicts and resolutions
- Plan character interactions across multiple chapters
- Ensure each character has a purpose in the story

GUIDELINES:
- Age-appropriate for children 4-10
- Diverse backgrounds and abilities
- Positive traits: kindness, courage, curiosity, determination
- Relatable challenges children face
- Clear character development arcs
- Engaging personalities that drive plot forward

Always provide comprehensive character profiles that will support a full 10+ page story with multiple chapters.""",
        )
    
    def get_agent(self):
        return self.agent
    
    def create_characters(self, genre: str):
        characters = []
        if genre == "fantasy":
            characters = [
                {"name": "Elara", "type": "elf", "trait": "wise"},
                {"name": "Thorn", "type": "dragon", "trait": "fierce"},
                {"name": "Bramble", "type": "fairy", "trait": "playful"},
            ]
        elif genre == "adventure":
            characters = [
                {"name": "Jack", "type": "explorer", "trait": "brave"},
                {"name": "Luna", "type": "pirate", "trait": "clever"},
                {"name": "Finn", "type": "treasure hunter", "trait": "determined"},
            ]
        elif genre == "mystery":
            characters = [
                {"name": "Detective Sam", "type": "detective", "trait": "observant"},
                {"name": "Maggie", "type": "journalist", "trait": "curious"},
                {"name": "Mr. Whiskers", "type": "cat", "trait": "sneaky"},
            ]
        else:
            characters = [
                {"name": "Charlie", "type": "child", "trait": "imaginative"},
                {"name": "Riley", "type": "dog", "trait": "loyal"},
            ]
        return characters