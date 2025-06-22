# app/prompt_templates.py

def format_prompt(query: str, context_chunks: list[str], role_description: str) -> str:
    """Format a concise prompt optimized for smaller models."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    prompt = f"""You are {role_description}

Context: {relevant_context}

User: {query}

You:"""
    
    return prompt
