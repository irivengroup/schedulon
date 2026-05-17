from __future__ import annotations

from pathlib import Path


def test_seed_demo_flushes_parent_before_target_insert():
    content = Path("src/schedulon/application/services.py").read_text(encoding="utf-8")
    seed_start = content.index("def seed_demo")
    import_targets_start = content.index("def create_job")
    seed_body = content[seed_start:import_targets_start]
    assert "db.flush()" in seed_body
    assert "db.rollback()" in seed_body
