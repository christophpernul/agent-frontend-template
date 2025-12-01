#!/usr/bin/env python3
"""
CLI script to run the AI Agent.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from main import main_gradio

if __name__ == "__main__":
    main_gradio()
