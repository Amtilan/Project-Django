from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Product:
    id: int
    title: str
    description: str
    created_at: datetime 
    updated_at: datetime
    tags: list[str]=field(default_factory=list)