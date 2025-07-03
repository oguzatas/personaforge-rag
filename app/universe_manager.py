import json
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel, Field

data_required_fields = ["universe_name", "description", "roles"]
role_required_fields = ["name", "description"]
char_required_fields = ["name", "role", "universe", "inventory", "current_mood", "backstory", "location"]
mood_required_fields = ["primary_emotion", "intensity", "plutchik_axis"]

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
SYSTEM_DIR = DATA_DIR / "system"
UNIVERSES_DIR = DATA_DIR / "universes"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
SYSTEM_DIR.mkdir(exist_ok=True)
UNIVERSES_DIR.mkdir(exist_ok=True)

def validate_universe_manifest(manifest: dict):
    for field in data_required_fields:
        if field not in manifest:
            raise ValueError(f"Universe manifest missing required field: {field}")
    for role in manifest["roles"]:
        for rfield in role_required_fields:
            if rfield not in role:
                raise ValueError(f"Role missing required field: {rfield}")

def validate_character_manifest(char: dict):
    for field in char_required_fields:
        if field not in char:
            raise ValueError(f"Character manifest missing required field: {field}")
    mood = char["current_mood"]
    for mfield in mood_required_fields:
        if mfield not in mood:
            raise ValueError(f"Character mood missing required field: {mfield}")

def list_universes():
    """List all valid universes (directories containing manifest.json)."""
    valid_universes = []
    for d in UNIVERSES_DIR.iterdir():
        if d.is_dir() and (d / "manifest.json").exists():
            try:
                # Validate the manifest file
                with open(d / "manifest.json", encoding="utf-8") as f:
                    manifest = json.load(f)
                validate_universe_manifest(manifest)
                valid_universes.append(d.name)
            except (json.JSONDecodeError, ValueError, FileNotFoundError):
                # Skip invalid manifests
                continue
    return valid_universes

def create_universe(universe_data: Dict[str, Any]) -> None:
    """Create a new universe with manifest."""
    validate_universe_manifest(universe_data)
    universe_name = universe_data["universe_name"]
    universe_dir = UNIVERSES_DIR / universe_name
    universe_dir.mkdir(parents=True, exist_ok=True)
    
    # Create characters directory
    (universe_dir / "characters").mkdir(exist_ok=True)
    
    # Create faiss_index directory
    (universe_dir / "faiss_index").mkdir(exist_ok=True)
    
    # Save manifest
    manifest_path = universe_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(universe_data, f, indent=2, ensure_ascii=False)

def load_universe_manifest(universe: str):
    manifest_path = UNIVERSES_DIR / universe / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Universe '{universe}' not found")
    
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    validate_universe_manifest(manifest)
    return manifest

def create_character(character_data: Dict[str, Any]) -> None:
    """Create a new character."""
    validate_character_manifest(character_data)
    universe = character_data["universe"]
    char_name = character_data["name"].lower().replace(" ", "_")
    
    char_dir = UNIVERSES_DIR / universe / "characters"
    char_path = char_dir / f"{char_name}.json"
    
    with open(char_path, "w", encoding="utf-8") as f:
        json.dump(character_data, f, indent=2, ensure_ascii=False)

def load_characters(universe: str):
    char_dir = UNIVERSES_DIR / universe / "characters"
    if not char_dir.exists():
        return []
    
    characters = []
    for char_file in char_dir.glob("*.json"):
        with open(char_file, encoding="utf-8") as f:
            char = json.load(f)
            validate_character_manifest(char)
            characters.append(char)
    return characters

def get_character_by_name(universe: str, character_name: str) -> Dict[str, Any]:
    """Get a specific character by name."""
    characters = load_characters(universe)
    for char in characters:
        if char["name"].lower() == character_name.lower():
            return char
    raise ValueError(f"Character '{character_name}' not found in universe '{universe}'")

def create_character_registry(universe: str) -> Dict[str, Any]:
    """Create a registry of all characters in a universe for fast lookups."""
    characters = load_characters(universe)
    registry = {
        "universe": universe,
        "character_count": len(characters),
        "characters": {}
    }
    
    for char in characters:
        registry["characters"][char["name"]] = {
            "role": char["role"],
            "location": char["location"],
            "file_path": f"characters/{char['name'].lower().replace(' ', '_')}.json",
            "last_updated": None  # Could be enhanced with file modification time
        }
    
    # Save registry
    registry_path = UNIVERSES_DIR / universe / "character_registry.json"
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    return registry

def get_character_registry(universe: str) -> Dict[str, Any]:
    """Get the character registry for a universe."""
    registry_path = UNIVERSES_DIR / universe / "character_registry.json"
    if not registry_path.exists():
        return create_character_registry(universe)
    
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f) 