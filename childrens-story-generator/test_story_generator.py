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
    """Test the story generation functionality"""
    print("Testing Children's Story Generator...")
    
    try:
        # Create story generator
        generator = StoryGenerator()
        
        # Test story generation
        title = "The Magic Garden"
        genre = "Fantasy"
        
        print(f"Generating story: '{title}' in {genre} genre...")
        story = generator.generate_story(title, genre)
        
        print("\n" + "="*50)
        print("GENERATED STORY:")
        print("="*50)
        print(story)
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_story_generation())
    
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)