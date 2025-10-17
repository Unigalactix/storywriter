import streamlit as st
import sys
import os
import traceback

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
        
        # Add API status check
        with st.expander("🔧 API Status", expanded=False):
            try:
                from config import OPENAI_API_KEY
                if OPENAI_API_KEY and OPENAI_API_KEY.startswith('sk-'):
                    st.success("✅ API Key configured")
                else:
                    st.error("❌ API Key not configured properly")
                    st.info("Please check your .env file")
            except Exception as e:
                st.error(f"❌ Configuration error: {str(e)}")
    
    with col2:
        st.markdown("#### Generated Story")
        
        # Story output area
        if generate_clicked:
            if title.strip():
                # Show progress
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                try:
                    progress_text.text("🤖 Initializing AI agents...")
                    progress_bar.progress(25)
                    
                    # Initialize the story generator
                    story_gen = StoryGenerator()
                    
                    progress_text.text("👥 Character Developer is creating characters...")
                    progress_bar.progress(50)
                    
                    # Generate the story
                    story = story_gen.generate_story(title.strip(), genre)
                    
                    progress_text.text("✍️ Story Writer is crafting the narrative...")
                    progress_bar.progress(75)
                    
                    progress_text.text("🎬 Climax Creator is adding the exciting ending...")
                    progress_bar.progress(100)
                    
                    # Clear progress indicators
                    progress_text.empty()
                    progress_bar.empty()
                    
                    # Display the story
                    if story and len(story.strip()) > 50:
                        st.success("🎉 Story generated successfully!")
                        
                        # Story display
                        st.text_area(
                            "Your Magical Story:",
                            value=story,
                            height=400,
                            help="Your generated story appears here"
                        )
                        
                        # Add download button
                        st.download_button(
                            label="📥 Download Story",
                            data=story,
                            file_name=f"{title.replace(' ', '_')}_story.txt",
                            mime="text/plain"
                        )
                        
                        # Story statistics
                        word_count = len(story.split())
                        char_count = len(story)
                        
                        col_stats1, col_stats2 = st.columns(2)
                        with col_stats1:
                            st.metric("Word Count", word_count)
                        with col_stats2:
                            st.metric("Character Count", char_count)
                            
                    else:
                        st.error("❌ Failed to generate a complete story. Please try again with a different title.")
                        if story:
                            st.text_area("Partial output received:", value=story, height=200)
                        
                except Exception as e:
                    # Clear progress indicators
                    progress_text.empty()
                    progress_bar.empty()
                    
                    st.error(f"❌ Error generating story: {str(e)}")
                    
                    # Show detailed error in expander for debugging
                    with st.expander("🔍 Detailed Error Information", expanded=False):
                        st.text(traceback.format_exc())
                    
                    st.info("💡 Troubleshooting tips:")
                    st.markdown("""
                    - Check your internet connection
                    - Verify your OpenAI API key is valid and has credits
                    - Try a simpler title or different genre
                    - Make sure all required packages are installed
                    """)
            else:
                st.warning("⚠️ Please enter a title for your story.")
        else:
            st.info("👆 Enter a title and click 'Generate Story' to create your magical tale!")
    
    # Add sidebar with information
    with st.sidebar:
        st.markdown("### 🤖 About the AI Agents")
        st.markdown("""
        This app uses three specialized AI agents working together:
        
        **👥 Character Developer**
        - Creates engaging, diverse characters
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
        - Average length: 300-500 words
        """)
        
        st.markdown("### 🔧 Technical Info")
        st.markdown("""
        - **Framework**: AutoGen SelectorGroupChat
        - **Model**: GPT-4o-mini
        - **Agent Coordination**: Round-robin with selector
        - **Termination**: Auto-stop when complete
        """)

if __name__ == "__main__":
    main()