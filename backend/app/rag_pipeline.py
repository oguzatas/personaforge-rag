# app/rag_pipeline.py
from app.retriever import get_relevant_docs_for_universe
from app.prompt_templates import format_prompt_character_focused
from app.llm_interface import call_llm
from app.universe_manager import list_universes, load_universe_manifest, load_characters
from app.character import Character
from app.conversation_manager import conversation_manager

def answer_question(query: str, universe: str, character: Character, debug: bool = False) -> dict:
    """Answer a question using RAG with conversation history and dynamic character state changes."""
    # Get relevant context chunks (limit to 3 for smaller models)
    context_chunks = get_relevant_docs_for_universe(query, universe, k=3)
    
    # Create enhanced character description with current state
    character_desc = f"{character.name}, a {character.role} from {character.location}"
    
    # Get conversation history
    conversation_history = conversation_manager.format_conversation_context(character.name, universe)
    
    # Get important events for long-term memory
    important_events = conversation_manager.format_important_events(character.name, universe)
    
    # Add current character state to context
    character_state = f"Current mood: {character.describe_mood()}\nInventory: {', '.join(character.inventory) if character.inventory else 'Empty'}"
    
    # Format the full prompt with enhanced context
    full_prompt = format_prompt_character_focused(
        query, context_chunks, character_desc, conversation_history, 
        important_events, character_state
    )
    
    # Generate response
    response = call_llm(full_prompt)
    
    # Add messages to conversation history
    conversation_manager.add_message(character.name, universe, "user", query)
    conversation_manager.add_message(character.name, universe, "assistant", response)
    
    # Analyze conversation for character state changes
    emotion_changes, inventory_changes = conversation_manager.analyze_conversation_for_changes(
        character, query, response
    )
    
    # Apply changes to character
    changes_made = conversation_manager.apply_character_changes(
        character, emotion_changes, inventory_changes
    )
    
    # Save conversations and events
    conversation_manager.save_conversations()
    conversation_manager.save_character_events()
    
    if debug:
        return {
            "response": response,
            "debug_info": {
                "query": query,
                "retrieved_context": context_chunks,
                "conversation_history": conversation_history,
                "important_events": important_events,
                "character_state": character_state,
                "emotion_changes": emotion_changes,
                "inventory_changes": inventory_changes,
                "changes_applied": changes_made,
                "character_info": {
                    "name": character.name,
                    "role": character.role,
                    "mood": character.describe_mood(),
                    "inventory": character.inventory,
                    "backstory": character.backstory,
                    "location": character.location
                },
                "full_prompt": full_prompt,
                "universe": universe
            }
        }
    else:
        return {
            "response": response,
            "character_updated": changes_made,
            "emotion_changes": emotion_changes,
            "inventory_changes": inventory_changes
        }

def clear_conversation(character_name: str, universe: str):
    """Clear conversation history for a character."""
    conversation_manager.clear_conversation(character_name, universe)
    conversation_manager.save_conversations()

def get_character_events(character_name: str, universe: str, max_events: int = 10):
    """Get important events for a character."""
    events = conversation_manager.get_important_events(character_name, universe, max_events)
    return [
        {
            "event_type": event.event_type,
            "description": event.description,
            "timestamp": event.timestamp.isoformat(),
            "details": event.details
        }
        for event in events
    ]

if __name__ == "__main__":
    # Load existing conversations and events
    conversation_manager.load_conversations()
    conversation_manager.load_character_events()
    
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
        print(f"Important Events: {result['debug_info']['important_events']}")
        print(f"Character State: {result['debug_info']['character_state']}")
        print(f"Emotion Changes: {result['debug_info']['emotion_changes']}")
        print(f"Inventory Changes: {result['debug_info']['inventory_changes']}")
        print(f"Changes Applied: {result['debug_info']['changes_applied']}")
        print(f"Full Prompt: {result['debug_info']['full_prompt']}")
