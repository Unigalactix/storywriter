from typing import Dict, Any
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agents.writer_agent import WriterAgent
from agents.character_agent import CharacterAgent
from agents.climax_agent import ClimaxAgent
from config import LLM_CONFIG
import asyncio

class StoryGenerator:
    """Main orchestrator for the multi-agent story generation system"""
    
    def __init__(self):
        # Create shared model client
        self.model_client = OpenAIChatCompletionClient(
            model=LLM_CONFIG["model"],
            api_key=LLM_CONFIG["api_key"],
            temperature=LLM_CONFIG["temperature"],
            max_tokens=LLM_CONFIG["max_tokens"]
        )
        
        # Initialize agents
        self.character_agent = CharacterAgent()
        self.writer_agent = WriterAgent()
        self.climax_agent = ClimaxAgent()
        
        # Setup termination conditions
        self.text_mention_termination = TextMentionTermination("TERMINATE")
        self.max_messages_termination = MaxMessageTermination(max_messages=15)
        self.termination = self.text_mention_termination | self.max_messages_termination
        
        # Custom selector prompt for story generation workflow
        self.selector_prompt = """Select an agent to perform the next task in story creation.

{roles}

Current conversation context:
{history}

Select an agent from {participants} to perform the next task.
Follow this workflow:
1. Character_Developer should create characters first
2. Story_Writer should write the complete story using those characters
3. Climax_Creator should enhance the story with an exciting climax and resolution

Only select one agent."""
    
    def generate_story(self, title: str, genre: str) -> str:
        """Generate a complete children's story using multi-agent collaboration"""
        try:
            # Create the SelectorGroupChat team
            team = SelectorGroupChat(
                participants=[
                    self.character_agent.get_agent(),
                    self.writer_agent.get_agent(),
                    self.climax_agent.get_agent()
                ],
                model_client=self.model_client,
                termination_condition=self.termination,
                selector_prompt=self.selector_prompt,
                allow_repeated_speaker=True
            )
            
            # Create the initial task prompt
            task = f"""
            Create a wonderful children's story with the following details:
            
            Title: "{title}"
            Genre: {genre}
            
            Please work together to create an engaging story suitable for children aged 4-10:
            
            1. Character_Developer: First, create 2-3 interesting characters for this {genre} story titled "{title}". Make them age-appropriate and inspiring.
            
            2. Story_Writer: Then, write a complete story (300-500 words) using these characters. Include a clear beginning, middle, and ending with positive messages.
            
            3. Climax_Creator: Finally, enhance the story with an exciting but safe climax that teaches a valuable lesson.
            
            End with "TERMINATE" when the complete story is ready.
            """
            
            # Run the team synchronously (since Streamlit doesn't work well with async)
            result = asyncio.run(self._run_team_async(team, task))
            
            # Extract and return the story
            return self._extract_story_from_result(result)
            
        except Exception as e:
            return f"Sorry, there was an error generating the story: {str(e)}\n\nPlease check your API key and internet connection."
    
    async def _run_team_async(self, team, task):
        """Run the team asynchronously"""
        return await team.run(task=task)
    
    def _extract_story_from_result(self, result) -> str:
        """Extract the final story content from the team result"""
        try:
            if hasattr(result, 'messages') and result.messages:
                # Look for the longest message that likely contains the complete story
                story_content = ""
                for message in reversed(result.messages):
                    if hasattr(message, 'content') and message.content:
                        content = message.content
                        # Look for substantial content that looks like a story
                        if len(content) > 200 and any(word in content.lower() for word in ['once', 'story', 'tale', 'adventure']):
                            story_content = content
                            break
                
                if not story_content:
                    # Fallback: combine relevant messages
                    story_parts = []
                    for message in result.messages:
                        if hasattr(message, 'content') and message.content:
                            content = message.content
                            if len(content) > 50 and not content.startswith("Select an agent"):
                                story_parts.append(content)
                    
                    story_content = "\n\n".join(story_parts)
                
                # Clean up the content
                if "TERMINATE" in story_content:
                    story_content = story_content.replace("TERMINATE", "").strip()
                
                return story_content if story_content else "Unable to generate story. Please try again with a different title or genre."
            
            return "No story content was generated. Please try again."
            
        except Exception as e:
            return f"Error processing story result: {str(e)}"

# Legacy function for backward compatibility
def generate_story(title: str, genre: str) -> str:
    writer_agent = WriterAgent()
    character_agent = CharacterAgent()
    climax_agent = ClimaxAgent()

    characters = character_agent.create_characters(genre)
    plot = f"{title} involves {', '.join(characters)}."
    story = writer_agent.generate_story(plot)
    climax = climax_agent.generate_climax(story)

    final_story = f"{story}\n\nAnd then, the climax happens: {climax}"
    return final_story