class Character:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.role = data.get("role")
        self.universe = data.get("universe")
        self.inventory = data.get("inventory", [])
        self.current_mood = data.get("current_mood", {})
        self.backstory = data.get("backstory", "")
        self.location = data.get("location", "")
        
        # Enhanced schema fields
        self.personality_traits = data.get("personality_traits", [])
        self.key_quotes = data.get("key_quotes", [])
        self.knowledge_domains = data.get("knowledge_domains", [])
        self.relationships = data.get("relationships", {})
        self.metadata = data.get("metadata", {})

    def describe_mood(self):
        mood = self.current_mood
        if not mood:
            return "Mood unknown."
        return (
            f"Primary emotion: {mood.get('primary_emotion')}, "
            f"Intensity: {mood.get('intensity')}, "
            f"Plutchik axis: {', '.join(mood.get('plutchik_axis', []))}"
        )
    
    def describe_personality(self):
        """Describe character personality traits."""
        if not self.personality_traits:
            return "Personality traits not defined."
        return f"Personality: {', '.join(self.personality_traits)}"
    
    def describe_relationships(self):
        """Describe character relationships."""
        if not self.relationships:
            return "Relationships not defined."
        
        rel = self.relationships
        parts = []
        if rel.get('faction'):
            parts.append(f"Faction: {rel['faction']}")
        if rel.get('allies'):
            parts.append(f"Allies: {', '.join(rel['allies'])}")
        if rel.get('enemies'):
            parts.append(f"Enemies: {', '.join(rel['enemies'])}")
        
        return "; ".join(parts) if parts else "No specific relationships defined."
    
    def describe_knowledge(self):
        """Describe character knowledge domains."""
        if not self.knowledge_domains:
            return "Knowledge domains not defined."
        return f"Knowledge: {', '.join(self.knowledge_domains)}"
    
    def get_quotes(self):
        """Get character's key quotes."""
        return self.key_quotes if self.key_quotes else []
    
    def to_dict(self):
        """Convert character to dictionary."""
        return {
            "name": self.name,
            "role": self.role,
            "universe": self.universe,
            "inventory": self.inventory,
            "current_mood": self.current_mood,
            "backstory": self.backstory,
            "location": self.location,
            "personality_traits": self.personality_traits,
            "key_quotes": self.key_quotes,
            "knowledge_domains": self.knowledge_domains,
            "relationships": self.relationships,
            "metadata": self.metadata
        }

    def __str__(self):
        return f"{self.name} the {self.role} at {self.location}" 