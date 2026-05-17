from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class JobDefinition:
    id: str
    name: str
