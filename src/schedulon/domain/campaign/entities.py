from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class CampaignReport:
    campaign_id: str
    status: str
