from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class Target:
    id: str
    name: str
    address: str
