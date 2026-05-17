# Changelog

## 1.0.0
- Consolidation complète de tous les incréments précédents.
- Le ZIP contient toute l’arborescence projet, pas seulement les deltas.


## 1.0.1

- Fixed GitHub Actions dependency installation issue.
- Added requirements.txt with editable install.
- Added complete GitHub Actions workflow.
- Lowered Python compatibility target to 3.9+.
- Added future annotations compatibility for Python 3.9.
- Replaced StrEnum with str/Enum compatibility.


## 1.0.2

- Added Python 3.13 and 3.14 compatibility in CI matrix.
- Added packaging validation with build + twine check.
- Enabled prerelease interpreter support for forward compatibility.


## 1.0.6

- Fixed Python 3.9 Alembic/Pydantic failure caused by `str | None` annotations.
- Rewrote Settings with `typing.Optional`.
- Added `eval-type-backport`.
- Added `flake8` to dev dependencies.
- Hardened CI by using `python -m flake8`, `python -m alembic`, and tool sanity checks.


## 1.0.6

- Fixed CI failure: `No module named build`.
- Installed CI tooling explicitly before running packaging checks.
- Added `requirements-ci.txt` for clarity.
- Moved packaging validation after lint, migration and tests in the matrix job.


## 1.0.6

- Fixed Python 3.9 SQLAlchemy/Alembic failure caused by `Mapped[datetime | None]`.
- Rewrote ORM models to use `Mapped[Optional[...]]`.
- Added a regression test for Python 3.9 ORM annotation compatibility.
- Added a CI guard to reject PEP 604 unions in SQLAlchemy mapped annotations.


## 1.0.6

- Fixed Docker/PostgreSQL seed-demo FK violation.
- Added explicit `db.flush()` after inserting `TargetSource`.
- Added rollback-on-error in write-side service functions.
- Added Docker-specific seed demo validation script.
- Added regression test for FK insertion ordering.
