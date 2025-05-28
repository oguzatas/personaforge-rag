# app/prompt_templates.py

def format_prompt(query: str, context_chunks: list[str], role_description: str) -> str:
    context = "\n\n".join(context_chunks)
    return f"""
{role_description}
Aşağıda bazı bilgiler var. Buna dayanarak oyuncunun sorusuna cevap ver:

=== Bilgiler ===
{context}

=== Soru ===
{query}

=== Cevap ===
"""
