# app/rag_pipeline.py
from app.retriever import get_relevant_docs_for_universe
from app.prompt_templates import format_prompt
from app.llm_interface import call_llm
from app.universe_manager import list_universes, load_universe_manifest, load_characters
from app.character import Character

def answer_question(query: str, universe: str, character: Character, debug: bool = False) -> dict:
    """Answer a question using RAG with optional debugging information."""
    # Get relevant context chunks
    context_chunks = get_relevant_docs_for_universe(query, universe)
    
    # Create simple character description
    character_desc = f"I am {character.name}, a {character.role} from {character.location}. My backstory: {character.backstory}"
    
    # Format the full prompt
    full_prompt = format_prompt(query, context_chunks, character_desc)
    
    # Generate response
    response = call_llm(full_prompt)
    
    if debug:
        return {
            "response": response,
            "debug_info": {
                "query": query,
                "retrieved_context": context_chunks,
                "character_info": {
                    "name": character.name,
                    "role": character.role,
                    "mood": character.describe_mood(),
                    "backstory": character.backstory,
                    "location": character.location
                },
                "full_prompt": full_prompt,
                "universe": universe
            }
        }
    else:
        return {"response": response}

if __name__ == "__main__":
    universes = list_universes()
    print(f"Available universes: {', '.join(universes)}")
    universe = input("Select universe: ")
    chars_data = load_characters(universe)
    characters = [Character(cd) for cd in chars_data]
    print("Available characters:")
    for idx, char in enumerate(characters):
        print(f"{idx+1}. {char}")
    char_idx = int(input("Select character number: ")) - 1
    character = characters[char_idx]
    while True:
        query = input("\nQuestion: ")
        if query.lower() in ["exit", "quit"]: break
        result = answer_question(query, universe, character, debug=True)
        print(f"\nAnswer: {result['response']}")
        print(f"\nDebug Info:")
        print(f"Retrieved Context: {result['debug_info']['retrieved_context']}")
        print(f"Full Prompt: {result['debug_info']['full_prompt']}")
