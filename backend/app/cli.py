#!/usr/bin/env python3
"""
CLI Tools for PersonaForge RAG System
Consolidated command-line interface for all system operations.
"""

import argparse
import sys
from pathlib import Path

from app.character_manager import CharacterManager
from app.universe_manager import list_universes, create_character_registry
from app.universe_embedder import build_universe_index, build_all_universe_indices


def character_cli():
    """Character management CLI commands."""
    parser = argparse.ArgumentParser(description="Character Management Commands")
    parser.add_argument("action", choices=[
        "create", "list", "show", "update", "delete", 
        "export", "import", "stats", "registry"
    ], help="Action to perform")
    parser.add_argument("--universe", "-u", required=True, 
                       help="Universe name")
    parser.add_argument("--character", "-c", 
                       help="Character name")
    parser.add_argument("--file", "-f",
                       help="File path (for export/import)")
    
    args = parser.parse_args()
    
    # Validate universe exists
    universes = list_universes()
    if args.universe not in universes:
        print(f"❌ Universe '{args.universe}' not found. Available: {', '.join(universes)}")
        return
    
    manager = CharacterManager()
    
    if args.action == "create":
        char_data = manager.create_character_interactive(args.universe)
        manager.create_character_from_data(char_data)
    elif args.action == "list":
        manager.list_characters(args.universe)
    elif args.action == "show":
        if not args.character:
            print("❌ Character name required for show action")
            return
        manager.show_character(args.universe, args.character)
    elif args.action == "update":
        if not args.character:
            print("❌ Character name required for update action")
            return
        print("Update functionality requires interactive input. Use the API for programmatic updates.")
    elif args.action == "delete":
        if not args.character:
            print("❌ Character name required for delete action")
            return
        manager.delete_character(args.universe, args.character)
    elif args.action == "export":
        if not args.character or not args.file:
            print("❌ Character name and file path required for export action")
            return
        manager.export_character(args.universe, args.character, args.file)
    elif args.action == "import":
        if not args.file:
            print("❌ File path required for import action")
            return
        manager.import_character(args.universe, args.file)
    elif args.action == "stats":
        stats = manager.get_character_stats(args.universe)
        print(f"\nCharacter Statistics for {args.universe}:")
        print(f"Total characters: {stats.get('total_characters', 0)}")
        print(f"Roles: {stats.get('roles', {})}")
        print(f"Locations: {stats.get('locations', {})}")
        print(f"Moods: {stats.get('moods', {})}")
        print(f"With personality traits: {stats.get('with_personality', 0)}")
        print(f"With relationships: {stats.get('with_relationships', 0)}")
        print(f"With key quotes: {stats.get('with_quotes', 0)}")
    elif args.action == "registry":
        registry = create_character_registry(args.universe)
        print(f"✅ Character registry created/updated for {args.universe}")
        print(f"Total characters: {registry['character_count']}")


def universe_cli():
    """Universe management CLI commands."""
    parser = argparse.ArgumentParser(description="Universe Management Commands")
    parser.add_argument("action", choices=[
        "list", "build-index", "build-all-indices"
    ], help="Action to perform")
    parser.add_argument("--universe", "-u", 
                       help="Universe name (for build-index)")
    
    args = parser.parse_args()
    
    if args.action == "list":
        universes = list_universes()
        if not universes:
            print("No universes found.")
            return
        print("Available universes:")
        for universe in universes:
            print(f"  - {universe}")
    
    elif args.action == "build-index":
        if not args.universe:
            print("❌ Universe name required for build-index action")
            return
        try:
            chunk_count = build_universe_index(args.universe)
            print(f"✅ FAISS index built for '{args.universe}' with {chunk_count} chunks")
        except Exception as e:
            print(f"❌ Error building index: {e}")
    
    elif args.action == "build-all-indices":
        try:
            build_all_universe_indices()
            print("✅ FAISS indices built for all universes")
        except Exception as e:
            print(f"❌ Error building indices: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PersonaForge RAG System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Character management
  python -m app.cli character create --universe Mytherra
  python -m app.cli character list --universe Mytherra
  python -m app.cli character show --universe Mytherra --character "Kael Vire"
  
  # Universe management
  python -m app.cli universe list
  python -m app.cli universe build-index --universe Mytherra
  python -m app.cli universe build-all-indices
        """
    )
    
    parser.add_argument("module", choices=["character", "universe"], 
                       help="Module to use")
    
    # Parse the module argument
    args, remaining = parser.parse_known_args()
    
    # Route to appropriate CLI
    if args.module == "character":
        # Set sys.argv to remaining args for character_cli
        sys.argv = [sys.argv[0]] + remaining
        character_cli()
    elif args.module == "universe":
        # Set sys.argv to remaining args for universe_cli
        sys.argv = [sys.argv[0]] + remaining
        universe_cli()


if __name__ == "__main__":
    main() 