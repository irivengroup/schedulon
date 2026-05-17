from __future__ import annotations
from enum import Enum
class ItsmProvider(str, Enum):
    GENERIC='generic'
    SERVICENOW='servicenow'
    JIRA_SERVICE_MANAGEMENT='jira_service_management'
