class Character:
    def __init__(self, data: dict):
        self.name = data.get("name")
        self.role = data.get("role")
        self.universe = data.get("universe")
        self.inventory = data.get("inventory", [])
        self.current_mood = data.get("current_mood", {})
        self.backstory = data.get("backstory", "")
        self.location = data.get("location", "")

    def describe_mood(self):
        mood = self.current_mood
        if not mood:
            return "Mood unknown."
        return (
            f"Primary emotion: {mood.get('primary_emotion')}, "
            f"Intensity: {mood.get('intensity')}, "
            f"Plutchik axis: {', '.join(mood.get('plutchik_axis', []))}"
        )

    def __str__(self):
        return f"{self.name} the {self.role} at {self.location}" 