#!/usr/bin/env python3
"""
Character Management CLI for PersonaForge RAG System
Provides command-line interface for managing characters.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.character_manager import CharacterManager, main

if __name__ == "__main__":
    main() 