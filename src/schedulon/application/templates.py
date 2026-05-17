from dataclasses import dataclass

@dataclass
class DryRunResult:
    template_name: str
    version: str
    impacted_targets: int
    rollback_defined: bool
    execution_allowed: bool
    summary: str

def simulate_campaign() -> DryRunResult:
    return DryRunResult(
        template_name="patch-linux-prod",
        version="12",
        impacted_targets=24,
        rollback_defined=True,
        execution_allowed=True,
        summary="Dry-run validated successfully"
    )
