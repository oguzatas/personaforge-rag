#!/usr/bin/env python3
"""
Test script for Character Manager functionality
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.character_manager import CharacterManager
from app.universe_manager import list_universes

def test_character_manager():
    """Test basic character manager functionality."""
    print("Testing Character Manager...")
    
    # Initialize manager
    manager = CharacterManager()
    
    # List available universes
    universes = list_universes()
    print(f"Available universes: {universes}")
    
    if not universes:
        print("No universes found. Please create a universe first.")
        return
    
    # Test with first available universe
    universe = universes[0]
    print(f"\nTesting with universe: {universe}")
    
    # Test listing characters
    print("\n1. Testing list characters:")
    characters = manager.list_characters(universe)
    
    # Test character stats
    print("\n2. Testing character stats:")
    stats = manager.get_character_stats(universe)
    print(f"Character statistics: {stats}")
    
    # Test showing a character if any exist
    if characters:
        first_char = characters[0]
        print(f"\n3. Testing show character: {first_char['name']}")
        char_details = manager.show_character(universe, first_char['name'])
        print(f"Character details retrieved: {char_details is not None}")
    
    print("\n✅ Character Manager tests completed!")

if __name__ == "__main__":
    test_character_manager() 