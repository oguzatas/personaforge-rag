#!/usr/bin/env python3
"""
Character Management CLI for PersonaForge RAG System
Legacy entry point - now uses consolidated CLI in app folder.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import and run the character CLI from the consolidated module
from app.cli import character_cli

if __name__ == "__main__":
    character_cli() 