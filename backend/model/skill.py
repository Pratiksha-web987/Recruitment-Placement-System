from dataclasses import dataclass


@dataclass
class Skill:
    skill_name: str
    category: str = None
    skill_id: int = None
    is_active: bool = True