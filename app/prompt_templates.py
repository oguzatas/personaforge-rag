# app/prompt_templates.py

def format_prompt(query: str, context_chunks: list[str], role_description: str, conversation_history: str = "") -> str:
    """Format a natural conversation prompt optimized for roleplay without prompt injection."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    # Build the prompt with conversation history if available
    if conversation_history:
        prompt = f"""{role_description}

Background: {relevant_context}

Recent conversation:
{conversation_history}

User: {query}

{role_description.split(',')[0]}:"""
    else:
        prompt = f"""{role_description}

Background: {relevant_context}

User: {query}

{role_description.split(',')[0]}:"""
    
    return prompt
