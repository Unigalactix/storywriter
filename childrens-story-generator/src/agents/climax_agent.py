import autogen
from config import LLM_CONFIG

class ClimaxAgent:
    """Agent responsible for creating exciting climaxes for children's stories"""
    
    def __init__(self):
        self.agent = autogen.AssistantAgent(
            name="Climax_Creator",
            system_message="""You are a master of creating exciting climaxes for children's stories. Your role is to:

1. Develop thrilling but age-appropriate climactic moments
2. Create tension and excitement suitable for children aged 4-10
3. Ensure climaxes lead to satisfying resolutions
4. Build emotional peaks that engage young readers
5. Incorporate character growth and lesson learning
6. Balance excitement with safety and positivity
7. Create memorable turning points in stories

Guidelines:
- Keep excitement age-appropriate (no scary or violent content)
- Focus on problem-solving, friendship, and courage
- Create moments where characters overcome challenges
- Include emotional satisfaction and character growth
- Build suspense through anticipation, not fear
- Ensure climaxes support the story's moral lesson
- Make climaxes relatable to children's experiences
- Create "wow" moments that children will remember

Always create climaxes that:
- Resolve the main conflict positively
- Show characters using their strengths
- Teach valuable life lessons
- Leave children feeling empowered and happy""",
            llm_config=LLM_CONFIG,
            human_input_mode="NEVER",
        )
    
    def get_agent(self):
        return self.agent
    
    def generate_climax(self, story: str) -> str:
        # This method generates a climax for the given story.
        # For simplicity, we will create a basic climax structure.
        climax = f"And just when everything seemed lost, {self.create_twist()}."
        return climax

    def create_twist(self) -> str:
        # This method creates a twist for the climax.
        twists = [
            "the hero discovered a hidden power within themselves",
            "a long-lost friend appeared to help",
            "the villain revealed their true intentions",
            "an unexpected ally joined the fight",
            "the hero realized that love was the greatest strength"
        ]
        import random
        return random.choice(twists)