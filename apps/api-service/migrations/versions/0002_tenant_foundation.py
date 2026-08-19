"""Add tenant identity and membership.

Revision ID: 0002_tenant_foundation
Revises: 0001_database_foundation
Create Date: 2026-08-19
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0002_tenant_foundation"
down_revision: str | None = "0001_database_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

tenant_status = postgresql.ENUM(
    "provisioning",
    "active",
    "suspended",
    "archived",
    name="tenant_status",
    create_type=False,
)
platform_role = postgresql.ENUM(
    "platform_owner",
    "platform_support",
    name="platform_role",
    create_type=False,
)
tenant_role = postgresql.ENUM(
    "tenant_owner",
    "tenant_admin",
    "tenant_staff",
    name="tenant_role",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    tenant_status.create(bind)
    platform_role.create(bind)
    tenant_role.create(bind)

    op.create_table(
        "tenants",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("status", tenant_status, nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "admin_users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("platform_role", platform_role, nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "email = lower(email)",
            name="ck_admin_users_email_lowercase",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "tenant_memberships",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("admin_user_id", sa.Uuid(), nullable=False),
        sa.Column("role", tenant_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["admin_user_id"],
            ["admin_users.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenants.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "admin_user_id",
            name="uq_tenant_memberships_tenant_admin_user",
        ),
    )
    op.create_index(
        op.f("ix_tenant_memberships_admin_user_id"),
        "tenant_memberships",
        ["admin_user_id"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_tenant_memberships_admin_user_id"),
        table_name="tenant_memberships",
    )
    op.drop_table("tenant_memberships")
    op.drop_table("admin_users")
    op.drop_table("tenants")

    bind = op.get_bind()
    tenant_role.drop(bind)
    platform_role.drop(bind)
    tenant_status.drop(bind)
