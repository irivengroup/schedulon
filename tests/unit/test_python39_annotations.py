from __future__ import annotations

from pathlib import Path


def test_sqlalchemy_models_do_not_use_pep604_unions():
    content = Path("src/schedulon/infrastructure/db/models.py").read_text(encoding="utf-8")
    assert " | None" not in content
    assert "Mapped[Optional[" in content
