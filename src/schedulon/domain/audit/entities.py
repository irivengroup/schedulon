from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class AuditEvent:
    actor_id: str|None
    action: str
