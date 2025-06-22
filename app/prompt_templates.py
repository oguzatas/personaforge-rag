# app/prompt_templates.py

def format_prompt(query: str, context_chunks: list[str], role_description: str) -> str:
    """Format a simple, plain English prompt for the LLM."""
    context = "\n".join(context_chunks)
    
    prompt = f"""You are roleplaying as a character. Respond naturally to the user's question.

Character: {role_description}

World Context: {context}

User: {query}

Character:"""
    
    return prompt
