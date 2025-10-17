import streamlit as st
import sys
import os

# Add the parent directory to the Python path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.story_generator import StoryGenerator
from config import GENRES, DEFAULT_GENRE

def main():
    st.set_page_config(
        page_title="Children's Story Generator",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Children's Story Generator")
    st.markdown("### Create magical stories with AI-powered storytelling agents!")
    
    # Create columns for better layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Story Settings")
        
        # Title input
        title = st.text_input(
            "📖 Story Title:",
            placeholder="Enter an exciting title for your story...",
            help="Give your story a creative and engaging title"
        )
        
        # Genre selection
        genre = st.selectbox(
            "🎭 Genre:",
            options=GENRES,
            index=GENRES.index(DEFAULT_GENRE),
            help="Choose the genre that best fits your story idea"
        )
        
        # Generate button
        generate_clicked = st.button(
            "✨ Generate Story",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.markdown("#### Generated Story")
        
        # Story output area
        if generate_clicked:
            if title.strip():
                with st.spinner("🤖 Our AI agents are collaborating to create your story..."):
                    try:
                        # Initialize the story generator
                        story_gen = StoryGenerator()
                        
                        # Generate the story
                        story = story_gen.generate_story(title.strip(), genre)
                        
                        # Display the story
                        st.text_area(
                            "Your Story:",
                            value=story,
                            height=400,
                            help="Your generated story will appear here"
                        )
                        
                        # Add download button
                        st.download_button(
                            label="📥 Download Story",
                            data=story,
                            file_name=f"{title.replace(' ', '_')}_story.txt",
                            mime="text/plain"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error generating story: {str(e)}")
                        st.info("Please check your API configuration and try again.")
            else:
                st.warning("⚠️ Please enter a title for your story.")
        else:
            st.info("👆 Enter a title and click 'Generate Story' to create your magical tale!")
    
    # Add sidebar with information
    with st.sidebar:
        st.markdown("### 🤖 About the AI Agents")
        st.markdown("""
        This app uses three specialized AI agents:
        
        **👥 Character Developer**
        - Creates engaging characters
        - Develops personalities and traits
        - Ensures age-appropriate content
        
        **✍️ Story Writer** 
        - Crafts the main narrative
        - Uses simple, clear language
        - Includes moral lessons
        
        **🎬 Climax Creator**
        - Designs exciting story peaks
        - Creates satisfying resolutions
        - Ensures positive outcomes
        """)
        
        st.markdown("### 🎯 Story Guidelines")
        st.markdown("""
        - Stories are designed for ages 4-10
        - Content is always positive and educational
        - Each story includes valuable life lessons
        - Language is simple and engaging
        """)

if __name__ == "__main__":
    main()