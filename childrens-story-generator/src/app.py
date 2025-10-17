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
    st.markdown("### Create magical 10+ page stories with AI-powered storytelling agents!")
    st.info("🎯 **NEW**: Generate comprehensive 10+ page stories (1500+ words) with rich character development and exciting adventures!")
    
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
            "✨ Generate 10+ Page Story",
            type="primary",
            use_container_width=True,
            help="Generate a comprehensive story with multiple chapters"
        )
        
        # Story length info
        with st.expander("📖 Story Details", expanded=False):
            st.markdown("""
            **What you'll get:**
            - 🎭 **Rich Characters**: 3-5 detailed main characters
            - 📚 **10+ Pages**: Approximately 1,500+ words
            - 🏗️ **5 Chapters**: Well-structured narrative
            - 🎯 **Character Growth**: Development arcs throughout
            - 🌟 **Exciting Climax**: Thrilling but age-appropriate
            - 💝 **Life Lessons**: Positive messages woven in
            
            **Estimated generation time:** 2-5 minutes
            """)
        
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
                    progress_text.text("🤖 Initializing AI agents for long-form story...")
                    progress_bar.progress(10)
                    
                    # Initialize the story generator
                    story_gen = StoryGenerator()
                    
                    progress_text.text("👥 Character Developer creating detailed profiles...")
                    progress_bar.progress(25)
                    
                    progress_text.text("✍️ Story Writer crafting multi-chapter narrative...")
                    progress_bar.progress(50)
                    
                    progress_text.text("🎬 Climax Creator adding exciting enhancements...")
                    progress_bar.progress(75)
                    
                    # Generate the story
                    story = story_gen.generate_story(title.strip(), genre)
                    
                    progress_text.text("� Finalizing your 10+ page story...")
                    progress_bar.progress(100)
                    
                    # Clear progress indicators
                    progress_text.empty()
                    progress_bar.empty()
                    
                    # Display the story
                    if story and len(story.strip()) > 800:  # Increased threshold for longer stories
                        st.success("🎉 Your 10+ page story is ready!")
                        
                        # Story display with better formatting
                        st.markdown("### 📖 Your Magical Story")
                        
                        # Create tabs for different views
                        tab1, tab2 = st.tabs(["📚 Read Story", "📊 Story Stats"])
                        
                        with tab1:
                            # Display story in a nice text area
                            st.text_area(
                                "Your Complete Story:",
                                value=story,
                                height=600,  # Increased height for longer stories
                                help="Your multi-chapter story appears here",
                                label_visibility="collapsed"
                            )
                        
                        with tab2:
                            # Story statistics
                            word_count = len(story.split())
                            char_count = len(story)
                            estimated_pages = max(10, word_count // 150)  # 150 words per page average
                            reading_time = max(5, word_count // 200)  # Average reading speed for children
                            
                            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                            with col_stats1:
                                st.metric("📝 Word Count", f"{word_count:,}")
                            with col_stats2:
                                st.metric("📄 Estimated Pages", estimated_pages)
                            with col_stats3:
                                st.metric("⏱️ Reading Time", f"{reading_time} min")
                            with col_stats4:
                                st.metric("🔤 Characters", f"{char_count:,}")
                            
                            # Reading level indicator
                            if word_count >= 1500:
                                st.success("✅ Meets 10+ page target!")
                            else:
                                st.warning(f"📏 Story is {word_count} words. Consider regenerating for fuller content.")
                        
                        # Download options
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button(
                                label="📥 Download as Text",
                                data=story,
                                file_name=f"{title.replace(' ', '_')}_story.txt",
                                mime="text/plain"
                            )
                        with col_dl2:
                            # Format story for better reading
                            formatted_story = f"# {title}\n\n{story}"
                            st.download_button(
                                label="📄 Download as Markdown",
                                data=formatted_story,
                                file_name=f"{title.replace(' ', '_')}_story.md",
                                mime="text/markdown"
                            )
                            
                    else:
                        st.error("❌ Failed to generate a complete 10+ page story. Please try again.")
                        if story:
                            st.text_area("Partial output received:", value=story, height=300)
                        
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
                st.warning("⚠️ Please enter a title for your 10+ page story.")
        else:
            st.info("👆 Enter a title and click 'Generate 10+ Page Story' to create your magical tale!")
            
            # Show example story structure
            with st.expander("📋 What makes a great 10+ page story?", expanded=False):
                st.markdown("""
                **Chapter Structure:**
                1. **Introduction** - Meet the characters and their world
                2. **Adventure Begins** - The main problem or quest starts
                3. **Challenges** - Characters face obstacles and grow
                4. **Climax** - The most exciting part with resolution
                5. **Conclusion** - Characters have learned and grown
                
                **Rich Characters:**
                - Detailed personalities and backgrounds
                - Clear goals and motivations
                - Growth throughout the story
                - Diverse and inclusive representation
                
                **Engaging Elements:**
                - Dialogue that brings characters to life
                - Vivid descriptions of settings and actions
                - Age-appropriate excitement and adventure
                - Positive life lessons woven naturally into the story
                """)
    
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
        
        st.markdown("### 🎯 Enhanced Story Features")
        st.markdown("""
        - **10+ Pages**: Comprehensive stories with 1,500+ words
        - **5 Chapters**: Well-structured narrative flow
        - **Rich Characters**: 3-5 detailed main characters with growth arcs
        - **Collaborative Creation**: Three AI agents working together
        - **Age-Appropriate**: Safe, positive content for ages 4-10
        - **Educational**: Life lessons integrated naturally
        - **Multiple Formats**: Download as text or markdown
        """)
        
        st.markdown("### 🔧 Technical Info")
        st.markdown("""
        - **Framework**: AutoGen SelectorGroupChat
        - **Model**: GPT-4o-mini with extended context
        - **Agent Coordination**: Multi-round collaboration
        - **Generation Time**: 2-5 minutes for full stories
        - **Termination**: Auto-stop when story is complete
        """)

if __name__ == "__main__":
    main()