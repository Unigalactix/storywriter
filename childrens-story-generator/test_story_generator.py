#!/usr/bin/env python3
"""
Test script for the Children's Story Generator
"""
import asyncio
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from components.story_generator import StoryGenerator

async def test_story_generation():
    """Test the 10+ page story generation functionality"""
    print("Testing Children's Story Generator - 10+ Page Stories...")
    
    try:
        # Create story generator
        generator = StoryGenerator()
        
        # Test story generation
        title = "The Magic Garden Adventure"
        genre = "Fantasy"
        
        print(f"Generating 10+ page story: '{title}' in {genre} genre...")
        print("⏳ This may take 2-5 minutes for a comprehensive story...")
        
        story = generator.generate_story(title, genre)
        
        print("\n" + "="*60)
        print("GENERATED 10+ PAGE STORY:")
        print("="*60)
        print(story)
        print("="*60)
        
        # Analyze the story
        word_count = len(story.split())
        estimated_pages = word_count // 150  # 150 words per page
        
        print(f"\n📊 STORY ANALYSIS:")
        print(f"📝 Word Count: {word_count:,}")
        print(f"📄 Estimated Pages: {estimated_pages}")
        print(f"🎯 Target Met: {'✅ Yes' if word_count >= 1500 else '❌ No'}")
        print(f"🔤 Character Count: {len(story):,}")
        
        # Check for story elements
        has_chapters = "chapter" in story.lower()
        has_dialogue = '"' in story or "'" in story
        has_characters = any(name_word in story.lower() for name_word in ["name", "character", "hero", "friend"])
        
        print(f"\n🎭 STORY ELEMENTS:")
        print(f"📚 Has Chapters: {'✅' if has_chapters else '❌'}")
        print(f"💬 Has Dialogue: {'✅' if has_dialogue else '❌'}")
        print(f"👥 Has Characters: {'✅' if has_characters else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_story_generation())
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)