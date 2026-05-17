from enum import StrEnum
class Role(StrEnum):
    ADMIN='admin'
    OPERATOR='operator'
    APPROVER='approver'
    VIEWER='viewer'
