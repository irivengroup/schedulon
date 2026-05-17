from __future__ import annotations

from functools import cached_property
from typing import Dict, List, Optional, Set

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = Field(default=8000, ge=1, le=65535)
    database_url: str = "postgresql+psycopg://schedulon:schedulon@localhost:5432/schedulon"

    security_secret_key: str = "dev-only-change-me-change-me-change-me"
    token_ttl_minutes: int = Field(default=60, ge=5, le=1440)
    auth_mode: str = "none"
    allowed_origins: str = ""

    ldap_uri: Optional[str] = None
    ldap_bind_dn: Optional[str] = None
    ldap_bind_password: Optional[str] = None
    ldap_user_base_dn: Optional[str] = None
    ldap_user_filter: str = "(uid={username})"
    ldap_group_base_dn: Optional[str] = None
    ldap_group_filter: str = "(member={user_dn})"
    ldap_allowed_groups: Optional[str] = None
    ldap_admin_group: Optional[str] = None
    ldap_operator_group: Optional[str] = None
    ldap_viewer_group: Optional[str] = None
    ldap_approver_group: Optional[str] = None

    report_default_recipients: str = ""
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from: str = "schedulon@example.net"
    webhook_url: Optional[str] = None
    slack_webhook_url: Optional[str] = None
    teams_webhook_url: Optional[str] = None

    worker_id: str = "worker-local"
    worker_poll_interval_seconds: int = 5
    scheduler_id: str = "scheduler-local"

    model_config = SettingsConfigDict(
        env_prefix="SCHEDULON_",
        env_file=".env",
        extra="ignore",
        frozen=True,
    )

    @field_validator("env")
    @classmethod
    def validate_env(cls, value: str) -> str:
        value = value.lower()
        if value not in {"development", "staging", "production"}:
            raise ValueError("Invalid environment")
        return value

    @field_validator("auth_mode")
    @classmethod
    def validate_auth_mode(cls, value: str) -> str:
        value = value.lower()
        if value not in {"none", "ldap"}:
            raise ValueError("Invalid auth mode")
        return value

    @model_validator(mode="after")
    def validate_prod(self):
        if self.env == "production":
            if len(self.security_secret_key) < 32 or self.security_secret_key.startswith("dev-only"):
                raise ValueError("Production requires strong SCHEDULON_SECURITY_SECRET_KEY")
            if self.auth_mode == "none":
                raise ValueError("Production requires authentication")
        return self

    @cached_property
    def allowed_origins_list(self) -> List[str]:
        return [x.strip() for x in self.allowed_origins.split(",") if x.strip()]

    def allowed_ldap_groups(self) -> Set[str]:
        if not self.ldap_allowed_groups:
            return set()
        return {x.strip().lower() for x in self.ldap_allowed_groups.split(";") if x.strip()}

    def default_report_recipients(self) -> List[str]:
        return [x.strip() for x in self.report_default_recipients.split(",") if x.strip()]
