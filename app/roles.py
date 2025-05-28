import json
from pathlib import Path

ROLES_FILE = Path(__file__).parent.parent / "roles.json"

def load_roles():
    with open(ROLES_FILE, encoding="utf-8") as f:
        return json.load(f)

def get_role_by_name(name: str):
    roles = load_roles()
    for role in roles:
        if role["name"] == name:
            return role
    raise ValueError(f"Role '{name}' not found.") 