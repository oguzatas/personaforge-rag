# app/rag_pipeline.py
from app.retriever import get_relevant_docs_for_universe
from app.prompt_templates import format_prompt
from app.llm_interface import call_llm
from app.universe_manager import list_universes, load_universe_manifest, load_characters
from app.character import Character
from app.conversation_manager import conversation_manager

def answer_question(query: str, universe: str, character: Character, debug: bool = False) -> dict:
    """Answer a question using RAG with conversation history."""
    # Get relevant context chunks (limit to 3 for smaller models)
    context_chunks = get_relevant_docs_for_universe(query, universe, k=3)
    
    # Create very concise character description
    character_desc = f"{character.name}, a {character.role} from {character.location}"
    
    # Get conversation history
    conversation_history = conversation_manager.format_conversation_context(character.name, universe)
    
    # Format the full prompt with conversation history
    full_prompt = format_prompt(query, context_chunks, character_desc, conversation_history)
    
    # Generate response
    response = call_llm(full_prompt)
    
    # Add messages to conversation history
    conversation_manager.add_message(character.name, universe, "user", query)
    conversation_manager.add_message(character.name, universe, "assistant", response)
    
    # Save conversations periodically
    conversation_manager.save_conversations()
    
    if debug:
        return {
            "response": response,
            "debug_info": {
                "query": query,
                "retrieved_context": context_chunks,
                "conversation_history": conversation_history,
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

def clear_conversation(character_name: str, universe: str):
    """Clear conversation history for a character."""
    conversation_manager.clear_conversation(character_name, universe)
    conversation_manager.save_conversations()

if __name__ == "__main__":
    # Load existing conversations
    conversation_manager.load_conversations()
    
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
        print(f"Conversation History: {result['debug_info']['conversation_history']}")
        print(f"Full Prompt: {result['debug_info']['full_prompt']}")
