from dataclasses import dataclass
@dataclass(frozen=True)
class JobRun:
    id: str
    status: str
