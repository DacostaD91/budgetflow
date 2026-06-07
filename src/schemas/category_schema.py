from dataclasses import dataclass


@dataclass
class CategoryCreateSchema:
    name: str
    type: str
    description: str | None = None
