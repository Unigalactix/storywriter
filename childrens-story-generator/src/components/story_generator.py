from typing import Dict, Any
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agents.writer_agent import WriterAgent
from agents.character_agent import CharacterAgent
from agents.climax_agent import ClimaxAgent
from config import LLM_CONFIG, TEAM_CONFIG, STORY_CONFIG
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
        
        # Setup termination conditions for longer collaboration
        self.text_mention_termination = TextMentionTermination("STORY_COMPLETE")
        self.max_messages_termination = MaxMessageTermination(max_messages=TEAM_CONFIG["max_messages"])
        self.termination = self.text_mention_termination | self.max_messages_termination
        
        # Enhanced selector prompt for collaborative story creation
        self.selector_prompt = """Select an agent to perform the next task in creating a comprehensive 10+ page children's story.

{roles}

Current conversation context:
{history}

Select an agent from {participants} to perform the next task.

COLLABORATIVE WORKFLOW:
1. Character_Developer: Create detailed character profiles and relationships
2. Story_Writer: Write the full story structure with chapters
3. Climax_Creator: Enhance with exciting moments and climaxes
4. Repeat collaboration to refine and improve the story

The goal is a complete, engaging 10+ page story (1500+ words) with rich characters and exciting plot developments.
Only select one agent at a time."""
    
    def generate_story(self, title: str, genre: str) -> str:
        """Generate a comprehensive 10+ page children's story using multi-agent collaboration"""
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
            
            # Create comprehensive task prompt for 10+ page story
            task = f"""
            Create a comprehensive children's story that will be at least 10 pages long (1500+ words):
            
            📚 STORY DETAILS:
            Title: "{title}"
            Genre: {genre}
            Target: 10+ pages (approximately 1500+ words)
            Structure: 5 chapters with 2 pages each
            Audience: Children aged 4-10
            
            🎯 COLLABORATION REQUIREMENTS:
            
            PHASE 1 - CHARACTER DEVELOPMENT:
            Character_Developer: Create 3-5 detailed main characters with:
            - Full character profiles with names, ages, personalities
            - Character relationships and dynamics
            - Character growth arcs for the full story
            - Supporting characters as needed
            - Character goals and challenges to overcome
            
            PHASE 2 - STORY WRITING:
            Story_Writer: Write the complete story with:
            - 5 chapters (approximately 300 words each)
            - Chapter 1: Introduction & Character Setup
            - Chapter 2: Adventure/Problem Begins
            - Chapter 3: Challenges & Character Development
            - Chapter 4: Climax & Resolution
            - Chapter 5: Conclusion & Life Lesson
            - Rich dialogue and vivid descriptions
            - Consistent character development throughout
            
            PHASE 3 - CLIMAX ENHANCEMENT:
            Climax_Creator: Enhance the story with:
            - Exciting moments in each chapter
            - Build tension throughout the story
            - Create memorable climactic sequence
            - Ensure satisfying resolution
            - Add "wow" moments that children will love
            
            FINAL REQUIREMENTS:
            - Minimum 1500 words total
            - Age-appropriate content with positive messages
            - Rich character development
            - Engaging plot with proper pacing
            - Clear moral lessons integrated naturally
            - Exciting but safe adventures
            - Satisfying conclusion
            
            Work together through multiple rounds to create a story that children will want to read again and again!
            
            When the complete 10+ page story is ready, end with "STORY_COMPLETE"
            """
            
            # Run the team with extended timeout for longer stories
            result = self._run_team_sync(team, task)
            
            # Extract and return the story
            return self._extract_story_from_result(result)
            
        except Exception as e:
            return f"Sorry, there was an error generating the story: {str(e)}\n\nPlease check your API key and internet connection. For longer stories, ensure you have sufficient API credits."
    
    def _run_team_sync(self, team, task):
        """Run the team synchronously using asyncio"""
        import asyncio
        try:
            # Try to get existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If event loop is running, we need to use a different approach
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(team.run(task=task))
            else:
                return asyncio.run(team.run(task=task))
        except RuntimeError:
            # No event loop, create new one
            return asyncio.run(team.run(task=task))
    
    async def _run_team_async(self, team, task):
        """Run the team asynchronously"""
        return await team.run(task=task)
    
    def _extract_story_from_result(self, result) -> str:
        """Extract the final story content from the team result"""
        try:
            if hasattr(result, 'messages') and result.messages:
                # Look for the complete story content
                story_content = ""
                all_content = []
                
                for message in result.messages:
                    if hasattr(message, 'content') and message.content:
                        content = message.content
                        # Skip system/coordination messages
                        if not any(skip_word in content.lower() for skip_word in ['select an agent', 'perform the next task', 'story_complete']):
                            all_content.append(content)
                
                # Look for the longest continuous story content
                for content in reversed(all_content):
                    # Check if this looks like a complete story
                    if (len(content) > 800 and  # Longer content for 10+ page stories
                        any(story_word in content.lower() for story_word in ['chapter', 'once upon', 'story', 'adventure', 'tale']) and
                        content.count('.') > 10):  # Has substantial content
                        story_content = content
                        break
                
                # If no single long story found, combine relevant content
                if not story_content:
                    story_parts = []
                    character_content = ""
                    main_story = ""
                    enhancement_content = ""
                    
                    for content in all_content:
                        if len(content) > 100:
                            # Categorize content by likely source
                            if any(char_word in content.lower() for char_word in ['character', 'name:', 'personality', 'traits']):
                                character_content += content + "\n\n"
                            elif any(story_word in content.lower() for story_word in ['chapter', 'once upon', 'adventure', 'story begins']):
                                main_story += content + "\n\n"
                            elif any(climax_word in content.lower() for climax_word in ['climax', 'exciting', 'enhancement', 'tension']):
                                enhancement_content += content + "\n\n"
                            else:
                                story_parts.append(content)
                    
                    # Combine in logical order if we have categorized content
                    if main_story:
                        story_content = main_story
                        if enhancement_content and "enhancement" not in main_story.lower():
                            story_content += "\n\n" + enhancement_content
                    else:
                        story_content = "\n\n".join(story_parts) if story_parts else "\n\n".join(all_content)
                
                # Clean up the content
                if "STORY_COMPLETE" in story_content:
                    story_content = story_content.replace("STORY_COMPLETE", "").strip()
                
                # Validate story length
                word_count = len(story_content.split())
                if word_count < STORY_CONFIG["min_total_words"]:
                    story_content += f"\n\n[Note: This story contains {word_count} words. For a full 10+ page experience, consider generating again for more detailed content.]"
                
                return story_content if story_content else "Unable to generate a complete story. Please try again with a different title or genre."
            
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