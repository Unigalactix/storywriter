def validate_input(input: str) -> bool:
    """Validates the input for the story title and genre."""
    return isinstance(input, str) and len(input) > 0

def format_output(story: str) -> str:
    """Formats the generated story for display."""
    return story.strip() if story else "No story generated."