import autogen
from config import LLM_CONFIG

class CharacterAgent:
    """Agent responsible for developing characters for children's stories"""
    
    def __init__(self):
        self.agent = autogen.AssistantAgent(
            name="Character_Developer",
            system_message="""You are a creative character developer for children's stories. Your role is to:

1. Create engaging, relatable characters appropriate for children aged 4-10
2. Develop character personalities, appearances, and motivations
3. Ensure characters are diverse, inclusive, and positive role models
4. Add character backstories that enhance the plot
5. Create character relationships and dynamics
6. Make characters memorable and loveable

Guidelines:
- Characters should be age-appropriate and inspiring
- Include diverse backgrounds and abilities
- Focus on positive traits like kindness, courage, curiosity
- Avoid scary or inappropriate elements
- Make characters relatable to children's experiences
- Keep descriptions vivid but simple

Always respond with detailed character profiles including:
- Name and basic description
- Personality traits
- Special abilities or talents
- Role in the story
- Character arc or growth""",
            llm_config=LLM_CONFIG,
            human_input_mode="NEVER",
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