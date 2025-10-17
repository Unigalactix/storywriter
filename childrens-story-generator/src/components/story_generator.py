import autogen
from typing import Dict, Any
from agents.writer_agent import WriterAgent
from agents.character_agent import CharacterAgent
from agents.climax_agent import ClimaxAgent
from config import LLM_CONFIG

class StoryGenerator:
    """Main orchestrator for the multi-agent story generation system"""
    
    def __init__(self):
        self.writer_agent = WriterAgent()
        self.character_agent = CharacterAgent()
        self.climax_agent = ClimaxAgent()
        
        # Create user proxy for managing the conversation
        self.user_proxy = autogen.UserProxyAgent(
            name="Story_Coordinator",
            system_message="You coordinate the story creation process between different agents.",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            code_execution_config=False,
        )
    
    def generate_story(self, title: str, genre: str) -> str:
        """Generate a complete children's story using multi-agent collaboration"""
        try:
            # Create the group chat with all agents
            groupchat = autogen.GroupChat(
                agents=[
                    self.character_agent.get_agent(),
                    self.writer_agent.get_agent(), 
                    self.climax_agent.get_agent(),
                    self.user_proxy
                ],
                messages=[],
                max_round=10,
                speaker_selection_method="round_robin"
            )
            
            # Create group chat manager
            manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=LLM_CONFIG)
            
            # Initial prompt to start the story generation process
            initial_prompt = f"""
            Let's create a wonderful children's story together!
            
            Title: "{title}"
            Genre: {genre}
            
            Please work together to create an engaging story:
            
            1. Character_Developer: First, create 2-3 interesting characters for this {genre} story titled "{title}". Make them age-appropriate for children 4-10.
            
            2. Story_Writer: Then, write a complete story using these characters. Include a beginning, middle, and ending. Keep it engaging but simple for young readers.
            
            3. Climax_Creator: Finally, enhance the story with an exciting but age-appropriate climax that teaches a valuable lesson.
            
            Let's begin!
            """
            
            # Start the conversation
            chat_result = self.user_proxy.initiate_chat(
                manager,
                message=initial_prompt,
            )
            
            # Extract the final story from the conversation
            story_content = self._extract_story_from_chat(chat_result)
            return story_content
            
        except Exception as e:
            return f"Sorry, there was an error generating the story: {str(e)}"
    
    def _extract_story_from_chat(self, chat_result) -> str:
        """Extract the final story content from the chat results"""
        if hasattr(chat_result, 'chat_history'):
            messages = chat_result.chat_history
        else:
            messages = []
        
        # Look for the final story in the last few messages
        story_content = ""
        for message in reversed(messages):
            if isinstance(message, dict) and 'content' in message:
                content = message['content']
                if len(content) > 200:  # Assume longer messages contain the story
                    story_content = content
                    break
        
        if not story_content and messages:
            # Fallback: combine all meaningful content
            story_parts = []
            for message in messages:
                if isinstance(message, dict) and 'content' in message:
                    content = message['content']
                    if len(content) > 50 and 'story' in content.lower():
                        story_parts.append(content)
            story_content = "\n\n".join(story_parts)
        
        return story_content if story_content else "Unable to generate story. Please try again."

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