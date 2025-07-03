"""
Character Manager Module for PersonaForge RAG System
Provides comprehensive character management functionality.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.universe_manager import (
    create_character, 
    load_characters, 
    get_character_by_name,
    create_character_registry,
    list_universes,
    UNIVERSES_DIR
)
from app.character import Character


class CharacterManager:
    """Comprehensive character management system."""
    
    def __init__(self):
        self.universes_dir = UNIVERSES_DIR
    
    def create_character_interactive(self, universe: str) -> Dict[str, Any]:
        """Interactive character creation with enhanced schema."""
        print(f"\nCreating character for universe: {universe}")
        
        # Basic character data
        char_data = {
            "universe": universe,
            "name": input("Character name: ").strip(),
            "role": input("Character role: ").strip(),
            "location": input("Character location: ").strip(),
            "backstory": input("Character backstory: ").strip(),
            "inventory": input("Inventory (comma-separated): ").strip().split(",") if input("Inventory (comma-separated): ").strip() else [],
            "current_mood": {
                "primary_emotion": input("Primary emotion: ").strip(),
                "intensity": input("Intensity (low/moderate/high): ").strip(),
                "plutchik_axis": input("Plutchik axis (comma-separated): ").strip().split(",") if input("Plutchik axis (comma-separated): ").strip() else []
            }
        }
        
        # Enhanced schema fields
        personality = input("Personality traits (comma-separated): ").strip()
        if personality:
            char_data["personality_traits"] = [t.strip() for t in personality.split(",")]
        
        quotes = input("Key quotes (comma-separated): ").strip()
        if quotes:
            char_data["key_quotes"] = [q.strip() for q in quotes.split(",")]
        
        knowledge = input("Knowledge domains (comma-separated): ").strip()
        if knowledge:
            char_data["knowledge_domains"] = [k.strip() for k in knowledge.split(",")]
        
        # Relationships
        faction = input("Faction: ").strip()
        allies = input("Allies (comma-separated): ").strip()
        enemies = input("Enemies (comma-separated): ").strip()
        
        if faction or allies or enemies:
            char_data["relationships"] = {
                "faction": faction if faction else None,
                "allies": [a.strip() for a in allies.split(",")] if allies else [],
                "enemies": [e.strip() for e in enemies.split(",")] if enemies else [],
                "mentor": None,
                "apprentices": []
            }
        
        # Metadata
        char_data["metadata"] = {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        return char_data
    
    def create_character_from_data(self, char_data: Dict[str, Any]) -> bool:
        """Create character from data dictionary."""
        try:
            create_character(char_data)
            print(f"✅ Character '{char_data['name']}' created successfully!")
            
            # Update registry
            create_character_registry(char_data['universe'])
            print(f"✅ Character registry updated for {char_data['universe']}")
            
            return True
        except Exception as e:
            print(f"❌ Error creating character: {e}")
            return False
    
    def list_characters(self, universe: str) -> List[Dict[str, Any]]:
        """List all characters in a universe with enhanced information."""
        try:
            characters = load_characters(universe)
            if not characters:
                print(f"No characters found in universe '{universe}'")
                return []
            
            print(f"\nCharacters in {universe}:")
            for i, char in enumerate(characters, 1):
                print(f"{i}. {char['name']} ({char['role']}) - {char['location']}")
                print(f"   Mood: {char['current_mood']['primary_emotion']} ({char['current_mood']['intensity']})")
                
                if 'personality_traits' in char:
                    print(f"   Personality: {', '.join(char['personality_traits'][:3])}...")
                
                if 'relationships' in char and char['relationships'].get('faction'):
                    print(f"   Faction: {char['relationships']['faction']}")
                
                print()
            
            return characters
            
        except Exception as e:
            print(f"❌ Error listing characters: {e}")
            return []
    
    def show_character(self, universe: str, character_name: str) -> Optional[Dict[str, Any]]:
        """Show detailed character information."""
        try:
            char = get_character_by_name(universe, character_name)
            print(f"\nCharacter: {char['name']}")
            print(f"Role: {char['role']}")
            print(f"Location: {char['location']}")
            print(f"Backstory: {char['backstory']}")
            print(f"Mood: {char['current_mood']['primary_emotion']} ({char['current_mood']['intensity']})")
            print(f"Inventory: {', '.join(char['inventory'])}")
            
            if 'personality_traits' in char:
                print(f"Personality: {', '.join(char['personality_traits'])}")
            if 'key_quotes' in char:
                print(f"Quotes: {' | '.join(char['key_quotes'])}")
            if 'knowledge_domains' in char:
                print(f"Knowledge: {', '.join(char['knowledge_domains'])}")
            if 'relationships' in char:
                rel = char['relationships']
                print(f"Faction: {rel.get('faction', 'None')}")
                if rel.get('allies'):
                    print(f"Allies: {', '.join(rel['allies'])}")
                if rel.get('enemies'):
                    print(f"Enemies: {', '.join(rel['enemies'])}")
            
            return char
                
        except Exception as e:
            print(f"❌ Error showing character: {e}")
            return None
    
    def update_character(self, universe: str, character_name: str, updates: Dict[str, Any]) -> bool:
        """Update character information."""
        try:
            char = get_character_by_name(universe, character_name)
            
            # Update fields
            for key, value in updates.items():
                if key in char:
                    char[key] = value
            
            # Update metadata
            if 'metadata' in char:
                char['metadata']['last_updated'] = datetime.now().isoformat()
            else:
                char['metadata'] = {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0"
                }
            
            # Save updated character
            char_name = char['name'].lower().replace(" ", "_")
            char_path = self.universes_dir / universe / "characters" / f"{char_name}.json"
            
            with open(char_path, "w", encoding="utf-8") as f:
                json.dump(char, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Character '{character_name}' updated successfully!")
            
            # Update registry
            create_character_registry(universe)
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating character: {e}")
            return False
    
    def delete_character(self, universe: str, character_name: str) -> bool:
        """Delete a character."""
        try:
            char = get_character_by_name(universe, character_name)
            char_name = char['name'].lower().replace(" ", "_")
            char_path = self.universes_dir / universe / "characters" / f"{char_name}.json"
            
            if char_path.exists():
                char_path.unlink()
                print(f"✅ Character '{character_name}' deleted successfully!")
                
                # Update registry
                create_character_registry(universe)
                return True
            else:
                print(f"❌ Character file not found: {char_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting character: {e}")
            return False
    
    def export_character(self, universe: str, character_name: str, output_path: str) -> bool:
        """Export character to a file."""
        try:
            char = get_character_by_name(universe, character_name)
            
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(char, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Character '{character_name}' exported to {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting character: {e}")
            return False
    
    def import_character(self, universe: str, import_path: str) -> bool:
        """Import character from a file."""
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                char_data = json.load(f)
            
            char_data["universe"] = universe
            
            return self.create_character_from_data(char_data)
            
        except Exception as e:
            print(f"❌ Error importing character: {e}")
            return False
    
    def get_character_stats(self, universe: str) -> Dict[str, Any]:
        """Get statistics about characters in a universe."""
        try:
            characters = load_characters(universe)
            
            stats = {
                "total_characters": len(characters),
                "roles": {},
                "locations": {},
                "moods": {},
                "with_personality": 0,
                "with_relationships": 0,
                "with_quotes": 0
            }
            
            for char in characters:
                # Role stats
                role = char.get('role', 'Unknown')
                stats['roles'][role] = stats['roles'].get(role, 0) + 1
                
                # Location stats
                location = char.get('location', 'Unknown')
                stats['locations'][location] = stats['locations'].get(location, 0) + 1
                
                # Mood stats
                mood = char.get('current_mood', {}).get('primary_emotion', 'Unknown')
                stats['moods'][mood] = stats['moods'].get(mood, 0) + 1
                
                # Enhanced features stats
                if 'personality_traits' in char:
                    stats['with_personality'] += 1
                if 'relationships' in char:
                    stats['with_relationships'] += 1
                if 'key_quotes' in char:
                    stats['with_quotes'] += 1
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting character stats: {e}")
            return {} 