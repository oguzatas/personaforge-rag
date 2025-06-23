# app/prompt_templates.py

def format_prompt(query: str, context_chunks: list[str], role_description: str, conversation_history: str = "") -> str:
    """Format a natural conversation prompt optimized for roleplay."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    # Build the prompt with conversation history if available
    if conversation_history:
        prompt = f"""You are {role_description}. Respond naturally as this character in conversation. Keep responses short and focused.

Your background: {relevant_context}

Recent conversation:
{conversation_history}

User says: {query}

Respond as your character:"""
    else:
        prompt = f"""You are {role_description}. Respond naturally as this character in conversation. Keep responses short and focused.

Your background: {relevant_context}

User says: {query}

Respond as your character:"""
    
    return prompt
