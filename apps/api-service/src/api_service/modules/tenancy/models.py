from datetime import datetime
from enum import StrEnum
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, validates

from api_service.infrastructure.database import (
    Base,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
)


def enum_values(enum_type: type[StrEnum]) -> list[str]:
    return [member.value for member in enum_type]


class TenantStatus(StrEnum):
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ARCHIVED = "archived"


class PlatformRole(StrEnum):
    PLATFORM_OWNER = "platform_owner"
    PLATFORM_SUPPORT = "platform_support"


class TenantRole(StrEnum):
    TENANT_OWNER = "tenant_owner"
    TENANT_ADMIN = "tenant_admin"
    TENANT_STAFF = "tenant_staff"


class Tenant(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(160))
    status: Mapped[TenantStatus] = mapped_column(
        Enum(
            TenantStatus,
            name="tenant_status",
            values_callable=enum_values,
        ),
        default=TenantStatus.PROVISIONING,
    )
    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class AdminUser(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "admin_users"
    __table_args__ = (
        CheckConstraint(
            "email = lower(email)",
            name="ck_admin_users_email_lowercase",
        ),
    )

    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    platform_role: Mapped[PlatformRole | None] = mapped_column(
        Enum(
            PlatformRole,
            name="platform_role",
            values_callable=enum_values,
        ),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    @validates("email")
    def normalize_email(self, _key: str, email: str) -> str:
        return email.strip().lower()


class TenantMembership(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tenant_memberships"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "admin_user_id",
            name="uq_tenant_memberships_tenant_admin_user",
        ),
    )

    tenant_id: Mapped[UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="RESTRICT"),
    )
    admin_user_id: Mapped[UUID] = mapped_column(
        ForeignKey("admin_users.id", ondelete="RESTRICT"),
        index=True,
    )
    role: Mapped[TenantRole] = mapped_column(
        Enum(
            TenantRole,
            name="tenant_role",
            values_callable=enum_values,
        ),
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
