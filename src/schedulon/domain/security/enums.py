from __future__ import annotations
from enum import Enum
class Role(str, Enum):
    ADMIN='admin'
    OPERATOR='operator'
    APPROVER='approver'
    VIEWER='viewer'
