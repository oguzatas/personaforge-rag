# app/prompt_templates.py

def format_prompt(query: str, context_chunks: list[str], role_description: str, conversation_history: str = "") -> str:
    """Format a concise prompt optimized for smaller models with conversation history."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    # Build the prompt with conversation history if available
    if conversation_history:
        prompt = f"""You are {role_description}

Context: {relevant_context}

Recent conversation:
{conversation_history}

User: {query}

You:"""
    else:
        prompt = f"""You are {role_description}

Context: {relevant_context}

User: {query}

You:"""
    
    return prompt
