"""
Main entry point for the AI Assistant application.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from src.constants import (
    ENV_VAR_NAME_SERVER_NAME,
    ENV_VAR_NAME_SERVER_PORT,
    ENV_VAR_NAME_MODEL_NAME,
    ENV_VAR_NAME_OPENAI_API_KEY,
    ENV_VAR_NAME_GOOGLE_API_KEY,
    APPLICATION_DESCRIPTION,
)
from src.utils.validation import check_requirements
from src.gradio_chat.gradio_app import create_app


def load_environment():
    """Load environment variables from .env file."""
    # Look for .env file in project root
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"

    if env_file.exists():
        load_dotenv(env_file, override=True)
    else:
        # Try to load from current directory
        load_dotenv(override=True)


def main_gradio():
    """Main application entry point for Gradio app."""
    print("Starting AI Assistant...")

    # Load environment variables
    load_environment()

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Get OpenAI API key and model name
    OPENAI_API_KEY = os.getenv(ENV_VAR_NAME_OPENAI_API_KEY)
    GEMINI_API_KEY = os.getenv(ENV_VAR_NAME_GOOGLE_API_KEY)
    LLM_MODEL_NAME = os.getenv(ENV_VAR_NAME_MODEL_NAME, "gpt-4o-mini")

    # Get port from environment variable
    SERVER_PORT = int(os.environ.get(ENV_VAR_NAME_SERVER_PORT, 7860))
    # Get server name (0.0.0.0 for Cloud Run, 127.0.0.1 for local)
    SERVER_NAME = os.environ.get(ENV_VAR_NAME_SERVER_NAME, "0.0.0.0")

    GEMINI_API_BASE_URL = os.environ.get("GEMINI_API_BASE_URL")
    OAUTH_GOOGLE_CLIENT_ID = os.environ.get("OAUTH_GOOGLE_CLIENT_ID")
    OAUTH_GOOGLE_CLIENT_SECRET = os.environ.get("OAUTH_GOOGLE_CLIENT_SECRET")

    if LLM_MODEL_NAME.startswith("gpt"):
        API_KEY: str = OPENAI_API_KEY
        BASE_URL = None
    elif LLM_MODEL_NAME.startswith("gemini"):
        API_KEY: str = GEMINI_API_KEY
        BASE_URL = GEMINI_API_BASE_URL

    # Create and launch the Gradio app
    app = create_app(API_KEY, LLM_MODEL_NAME)

    print("✅ AI Assistant is ready!")
    print("🌐 Opening web interface...")

    # Launch the app
    app.launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        share=False,  # Set to True if you want a public link
        show_error=True,
    )


if __name__ == "__main__":
    main_gradio()
