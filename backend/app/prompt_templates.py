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

def format_prompt_natural(query: str, context_chunks: list[str], role_description: str, conversation_history: str = "") -> str:
    """Alternative natural conversation format that's even more conversational."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    # Extract character name from role description
    character_name = role_description.split(',')[0].strip()
    
    # Build the prompt using very natural conversation format
    if conversation_history:
        prompt = f"""{character_name} is {role_description}

{character_name} lives in a world where: {relevant_context}

{conversation_history}

User: {query}

{character_name}:"""
    else:
        prompt = f"""{character_name} is {role_description}

{character_name} lives in a world where: {relevant_context}

User: {query}

{character_name}:"""
    
    return prompt

def format_prompt_simple(query: str, context_chunks: list[str], role_description: str, conversation_history: str = "") -> str:
    """Simplest format to minimize prompt injection."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    # Extract character name from role description
    character_name = role_description.split(',')[0].strip()
    
    # Build the prompt using minimal format
    if conversation_history:
        prompt = f"""{character_name}, {role_description}

{relevant_context}

{conversation_history}

User: {query}

{character_name}:"""
    else:
        prompt = f"""{character_name}, {role_description}

{relevant_context}

User: {query}

{character_name}:"""
    
    return prompt

def format_prompt_character_focused(query: str, context_chunks: list[str], role_description: str, 
                                   conversation_history: str = "", important_events: str = "", 
                                   character_state: str = "") -> str:
    """Enhanced prompt format with explicit character instructions and context guidance."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    # Extract character name from role description
    character_name = role_description.split(',')[0].strip()
    
    # Build context sections
    context_sections = []
    
    if relevant_context:
        context_sections.append(f"Background information: {relevant_context}")
    
    if character_state:
        context_sections.append(f"Your current state: {character_state}")
    
    if important_events:
        context_sections.append(important_events)
    
    if conversation_history:
        context_sections.append(f"Previous conversation:\n{conversation_history}")
    
    # Combine all context sections
    full_context = "\n\n".join(context_sections) if context_sections else ""
    
    # Build the prompt with explicit instructions
    prompt = f"""You are {character_name}, {role_description}

IMPORTANT: Always respond as {character_name}. Never break character or refer to yourself in third person. Use the background information to inform your responses naturally.

{full_context}

User: {query}

{character_name}:"""
    
    return prompt

def clean_response(response: str) -> str:
    """Clean the response to remove prompt injection artifacts and dialog continuation."""
    if not response:
        return response
    
    # Remove common prompt injection artifacts
    injection_patterns = [
        "You are",
        "User says:",
        "Respond as your character:",
        "Background:",
        "Background information:",
        "Previous conversation:",
        "Recent conversation:",
        "IMPORTANT:",
        "User:",
        "AI:",
        "BOT:",
        "SAM:",
        "Alex:"
    ]
    
    cleaned = response
    
    # Remove prompt injection patterns
    for pattern in injection_patterns:
        if pattern in cleaned:
            # Find the position of the pattern and remove everything before it
            pos = cleaned.find(pattern)
            if pos > 0:
                cleaned = cleaned[pos:]
                # Remove the pattern itself and everything after it
                cleaned = cleaned.replace(pattern, "", 1)
                # Find the next newline and remove everything up to it
                next_line = cleaned.find('\n')
                if next_line != -1:
                    cleaned = cleaned[next_line:].strip()
    
    # Remove dialog continuation patterns
    dialog_patterns = [
        "\nUser:",
        "\nAI:",
        "\nBOT:",
        "\nSAM:",
        "\nAlex:",
        "\nKael Vire:"
    ]
    
    for pattern in dialog_patterns:
        if pattern in cleaned:
            # Keep only the first response, remove everything after dialog continuation
            pos = cleaned.find(pattern)
            cleaned = cleaned[:pos]
    
    # Clean up extra whitespace and newlines
    cleaned = cleaned.strip()
    
    # If the response is too short after cleaning, return original
    if len(cleaned) < 10:
        return response
    
    return cleaned

def format_prompt_optimized(query: str, context_chunks: list[str], role_description: str, conversation_history: str = "") -> str:
    """Optimized prompt format that combines natural conversation with injection prevention."""
    # Take only the most relevant context (max 2 chunks)
    relevant_context = "\n".join(context_chunks[:2])
    
    # Extract character name from role description
    character_name = role_description.split(',')[0].strip()
    
    # Build the prompt using optimized format
    if conversation_history:
        prompt = f"""{character_name}, {role_description}

{relevant_context}

{conversation_history}

User: {query}

{character_name}:"""
    else:
        prompt = f"""{character_name}, {role_description}

{relevant_context}

User: {query}

{character_name}:"""
    
    return prompt
