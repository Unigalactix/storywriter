# 📚 Children's Story Generator

An AI-powered multi-agent system for generating engaging children's stories using the AutoGen framework and Streamlit.

## 🌟 Features

- **Multi-Agent Collaboration**: Three specialized AI agents work together to create comprehensive stories
- **Interactive Web Interface**: Easy-to-use Streamlit app with title input and genre selection
- **Child-Friendly Content**: Stories designed for ages 4-10 with positive messages and life lessons
- **Multiple Genres**: Fantasy, Adventure, Fairy Tale, Science Fiction, Mystery, and more
- **Download Stories**: Save generated stories as text files

## 🤖 AI Agents

### 👥 Character Developer
- Creates engaging, age-appropriate characters
- Develops personalities, traits, and relationships
- Ensures diverse and inclusive representation

### ✍️ Story Writer
- Transforms plots into complete narratives
- Uses simple, clear language for young readers
- Incorporates moral lessons naturally

### 🎬 Climax Creator
- Designs exciting but safe story climaxes
- Creates satisfying resolutions
- Ensures positive outcomes and character growth

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd childrens-story-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-4o-mini
   TEMPERATURE=0.7
   MAX_TOKENS=2000
   ```

4. **Run the application**
   ```bash
   cd src
   streamlit run app.py
   ```

5. **Access the app**
   Open your browser and go to `http://localhost:8501`

## 📖 How to Use

1. **Enter a Story Title**: Type in a creative title for your story
2. **Select a Genre**: Choose from Fantasy, Adventure, Fairy Tale, etc.
3. **Generate Story**: Click the button to let the AI agents create your story
4. **Read and Download**: Enjoy your story and download it if you like!

## Project Structure

```
childrens-story-generator
├── src
│   ├── app.py                  # Main entry point for the Streamlit application
│   ├── agents
│   │   ├── __init__.py         # Initializes the agents package
│   │   ├── writer_agent.py      # Contains the WriterAgent class
│   │   ├── character_agent.py    # Contains the CharacterAgent class
│   │   └── climax_agent.py      # Contains the ClimaxAgent class
│   ├── components
│   │   ├── __init__.py         # Initializes the components package
│   │   └── story_generator.py    # Contains the story generation logic
│   └── utils
│       ├── __init__.py         # Initializes the utils package
│       └── helpers.py           # Contains utility functions
├── requirements.txt             # Lists project dependencies
├── config.py                    # Contains configuration settings
└── README.md                    # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd childrens-story-generator
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command:

```bash
streamlit run src/app.py
```

Once the application is running, you can enter a title and genre for the story. The application will generate a children's story based on your input.

## Agents Overview

- **Writer Agent**: Responsible for generating the story based on the provided plot.
- **Character Agent**: Creates characters tailored to the specified genre.
- **Climax Agent**: Develops an engaging climax for the story.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.