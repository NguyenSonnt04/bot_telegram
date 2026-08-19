from uuid import uuid4

from sqlalchemy import CheckConstraint, UniqueConstraint

from api_service.modules.tenancy import (
    AdminUser,
    PlatformRole,
    TenantMembership,
    TenantRole,
    TenantStatus,
)


def test_tenancy_enums_match_product_contract() -> None:
    assert {status.value for status in TenantStatus} == {
        "provisioning",
        "active",
        "suspended",
        "archived",
    }
    assert {role.value for role in PlatformRole} == {
        "platform_owner",
        "platform_support",
    }
    assert {role.value for role in TenantRole} == {
        "tenant_owner",
        "tenant_admin",
        "tenant_staff",
    }


def test_admin_user_canonicalizes_email_to_lowercase() -> None:
    user = AdminUser(
        email="  OWNER@Example.COM ",
        password_hash="not-a-real-password-hash",
    )

    assert user.email == "owner@example.com"


def test_admin_user_table_enforces_lowercase_unique_email() -> None:
    constraints = AdminUser.__table__.constraints

    assert any(
        isinstance(constraint, CheckConstraint)
        and constraint.name == "ck_admin_users_email_lowercase"
        for constraint in constraints
    )
    assert AdminUser.__table__.c.email.unique is True


def test_membership_is_unique_per_tenant_and_admin_user() -> None:
    constraints = TenantMembership.__table__.constraints

    assert any(
        isinstance(constraint, UniqueConstraint)
        and constraint.name == "uq_tenant_memberships_tenant_admin_user"
        for constraint in constraints
    )
    assert (
        TenantMembership(
            tenant_id=uuid4(),
            admin_user_id=uuid4(),
            role=TenantRole.TENANT_OWNER,
        ).role
        is TenantRole.TENANT_OWNER
    )
