from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config import LLM_CONFIG

class WriterAgent:
    """Agent responsible for writing the complete children's story"""
    
    def __init__(self):
        # Create model client
        self.model_client = OpenAIChatCompletionClient(
            model=LLM_CONFIG["model"],
            api_key=LLM_CONFIG["api_key"],
            temperature=LLM_CONFIG["temperature"],
            max_tokens=LLM_CONFIG["max_tokens"]
        )
        
        self.agent = AssistantAgent(
            name="Story_Writer",
            description="Transforms story plots into engaging, complete stories for children aged 4-10 with positive messages",
            model_client=self.model_client,
            system_message="""You are a skilled children's story writer. Your role is to:

1. Transform story plots into engaging, complete stories for children aged 4-10
2. Write in simple, clear language appropriate for young readers
3. Create stories with positive messages and life lessons
4. Include dialogue, action, and descriptive elements
5. Structure stories with clear beginning, middle, and end
6. Incorporate characters and plot elements seamlessly
7. Maintain child-friendly tone throughout

Guidelines:
- Use vocabulary appropriate for children aged 4-10
- Keep sentences short and engaging
- Include moral lessons naturally within the story
- Avoid scary, violent, or inappropriate content
- Use repetition and rhythm to make stories memorable
- Create vivid but simple descriptions
- Include emotional connections children can relate to
- Aim for stories that are 300-500 words long

Always write complete, engaging stories that captivate young readers while teaching valuable life lessons.""",
        )
    
    def get_agent(self):
        return self.agent
    
    def generate_story(self, plot: str) -> str:
        # This method generates a complete children's story based on the provided plot.
        # For simplicity, we'll return a placeholder story.
        return f"Once upon a time, in a land where {plot}, there lived a brave little hero."