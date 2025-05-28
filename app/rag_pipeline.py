# app/rag_pipeline.py
from app.retriever import get_relevant_docs_for_universe
from app.prompt_templates import format_prompt
from app.llm_interface import call_llm
from app.universe_manager import list_universes, load_universe_manifest, load_characters
from app.character import Character

def answer_question(query: str, universe: str, character: Character) -> str:
    context_chunks = get_relevant_docs_for_universe(query, universe)
    # Use character's role and mood in the prompt
    role_desc = f"{character.name} ({character.role}) - {character.describe_mood()}\nBackstory: {character.backstory}"
    prompt = format_prompt(query, context_chunks, role_desc)
    response = call_llm(prompt)
    return response

if __name__ == "__main__":
    universes = list_universes()
    print(f"Mevcut evrenler: {', '.join(universes)}")
    universe = input("Evren seçin: ")
    chars_data = load_characters(universe)
    characters = [Character(cd) for cd in chars_data]
    print("Mevcut karakterler:")
    for idx, char in enumerate(characters):
        print(f"{idx+1}. {char}")
    char_idx = int(input("Karakter numarası seçin: ")) - 1
    character = characters[char_idx]
    while True:
        query = input("\n🧙 Soru: ")
        if query.lower() in ["exit", "quit"]: break
        answer = answer_question(query, universe, character)
        print(f"\n🤖 Cevap:\n{answer}")
