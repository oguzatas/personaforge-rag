from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

from app.universe_manager import (
    list_universes, create_universe, load_universe_manifest,
    create_character, load_characters, get_character_by_name
)
from app.character import Character
from app.rag_pipeline import answer_question
from app.universe_embedder import build_universe_index, build_all_universe_indices
from config.settings import FRONTEND_URL, API_HOST, API_PORT

app = FastAPI(title="PersonaForge RAG API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # Use config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UniverseCreate(BaseModel):
    universe_name: str
    description: str
    roles: List[Dict[str, str]]

class CharacterMood(BaseModel):
    primary_emotion: str
    intensity: str
    plutchik_axis: List[str]

class CharacterCreate(BaseModel):
    name: str
    role: str
    universe: str
    inventory: List[str]
    current_mood: CharacterMood
    backstory: str
    location: str

class ChatRequest(BaseModel):
    query: str
    universe: str
    character_name: str
    debug: bool = False

# Universe endpoints
@app.get("/api/universes")
async def get_universes():
    """Get all universes."""
    try:
        universes = list_universes()
        return {"universes": universes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/universes")
async def create_universe_endpoint(universe: UniverseCreate):
    """Create a new universe."""
    try:
        universe_data = universe.dict()
        create_universe(universe_data)
        return {"message": f"Universe '{universe.universe_name}' created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/universes/{universe_name}")
async def get_universe(universe_name: str):
    """Get universe details."""
    try:
        manifest = load_universe_manifest(universe_name)
        return manifest
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Character endpoints
@app.get("/api/universes/{universe_name}/characters")
async def get_characters(universe_name: str):
    """Get all characters in a universe."""
    try:
        characters = load_characters(universe_name)
        return {"characters": characters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/universes/{universe_name}/characters")
async def create_character_endpoint(universe_name: str, character: CharacterCreate):
    """Create a new character in a universe."""
    try:
        character_data = character.dict()
        character_data["universe"] = universe_name  # Ensure consistency
        create_character(character_data)
        return {"message": f"Character '{character.name}' created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/universes/{universe_name}/characters/{character_name}")
async def get_character(universe_name: str, character_name: str):
    """Get a specific character."""
    try:
        character = get_character_by_name(universe_name, character_name)
        return character
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Index building endpoints
@app.post("/api/universes/{universe_name}/build-index")
async def build_universe_index_endpoint(universe_name: str):
    """Build FAISS index for a specific universe."""
    try:
        chunk_count = build_universe_index(universe_name)
        return {"message": f"FAISS index built for '{universe_name}' with {chunk_count} chunks"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/build-all-indices")
async def build_all_indices_endpoint():
    """Build FAISS indices for all universes."""
    try:
        build_all_universe_indices()
        return {"message": "FAISS indices built for all universes"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat with a character using RAG."""
    try:
        character_data = get_character_by_name(request.universe, request.character_name)
        character = Character(character_data)
        result = answer_question(request.query, request.universe, character, debug=request.debug)
        
        if request.debug:
            return {
                "response": result["response"],
                "character": character_data["name"],
                "universe": request.universe,
                "debug_info": result["debug_info"]
            }
        else:
            return {
                "response": result["response"],
                "character": character_data["name"],
                "universe": request.universe
            }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check
@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT) 