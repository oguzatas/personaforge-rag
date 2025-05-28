from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from pathlib import Path
from app.faiss_manager import FaissManager
from app.universe_manager import load_characters, load_universe_manifest

MODEL_NAME = "all-MiniLM-L6-v2"

def build_universe_index(universe_name: str):
    """Build FAISS index for a specific universe using character data and lore."""
    print(f"Building FAISS index for universe: {universe_name}")
    
    model = SentenceTransformer(MODEL_NAME)
    
    # Collect text chunks from universe
    chunks = []
    
    # 1. Add universe description
    try:
        manifest = load_universe_manifest(universe_name)
        chunks.append(f"Universe: {manifest['universe_name']} - {manifest['description']}")
        
        # Add role descriptions
        for role in manifest['roles']:
            chunks.append(f"Role {role['name']}: {role['description']}")
    except Exception as e:
        print(f"Warning: Could not load universe manifest: {e}")
    
    # 2. Add character information
    try:
        characters = load_characters(universe_name)
        for char in characters:
            # Character description
            char_desc = f"Character: {char['name']} is a {char['role']} located at {char['location']}. "
            char_desc += f"Backstory: {char['backstory']} "
            char_desc += f"Current mood: {char['current_mood']['primary_emotion']} ({char['current_mood']['intensity']}). "
            char_desc += f"Inventory: {', '.join(char['inventory'])}"
            chunks.append(char_desc)
            
            # Separate backstory chunk for better retrieval
            chunks.append(f"{char['name']} backstory: {char['backstory']}")
            
            # Location information
            chunks.append(f"Location {char['location']}: {char['name']} the {char['role']} can be found here.")
    except Exception as e:
        print(f"Warning: Could not load characters: {e}")
    
    # 3. Check for additional lore files in universe directory
    universe_dir = Path("data") / universe_name
    lore_files = list(universe_dir.glob("*.txt")) + list(universe_dir.glob("*.md"))
    
    for lore_file in lore_files:
        try:
            with open(lore_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split into smaller chunks if the file is large
                if len(content) > 1000:
                    # Simple chunking by paragraphs
                    paragraphs = content.split('\n\n')
                    chunks.extend([p.strip() for p in paragraphs if p.strip()])
                else:
                    chunks.append(content)
        except Exception as e:
            print(f"Warning: Could not read lore file {lore_file}: {e}")
    
    if not chunks:
        # Create some default content if no data is found
        chunks = [
            f"This is the {universe_name} universe.",
            "No additional lore or character information is currently available."
        ]
        print("Warning: No content found, using default chunks.")
    
    print(f"Found {len(chunks)} text chunks to embed.")
    
    # Generate embeddings
    embeddings = model.encode(chunks, show_progress_bar=True)
    
    # Create and save FAISS index
    dim = embeddings.shape[1]
    faiss_manager = FaissManager(universe_name, dim)
    faiss_manager.create_index(np.array(embeddings))
    
    # Save chunks for retrieval
    chunks_path = Path("data") / universe_name / "faiss_index" / "chunks.txt"
    with open(chunks_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n---\n")
    
    print(f"✅ FAISS index built for {universe_name} with {len(chunks)} chunks.")
    return len(chunks)

def build_all_universe_indices():
    """Build FAISS indices for all universes."""
    from app.universe_manager import list_universes
    
    universes = list_universes()
    if not universes:
        print("No universes found.")
        return
    
    for universe in universes:
        try:
            build_universe_index(universe)
        except Exception as e:
            print(f"Error building index for {universe}: {e}")

if __name__ == "__main__":
    # Build indices for all universes
    build_all_universe_indices() 