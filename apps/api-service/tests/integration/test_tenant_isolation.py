import asyncio
import os
from uuid import uuid4

import pytest
from pydantic import SecretStr

from api_service.config import Settings
from api_service.infrastructure.database import DatabaseManager
from api_service.modules.tenancy import (
    AdminUser,
    Tenant,
    TenantContext,
    TenantMembership,
    TenantMembershipRepository,
    TenantRole,
)

REQUIRE_DATABASE_TESTS = "REQUIRE_DATABASE_TESTS"


def integration_settings() -> Settings:
    env_file = None if os.getenv(REQUIRE_DATABASE_TESTS) == "1" else ".env"
    return Settings(_env_file=env_file)


def isolation_database_url(settings: Settings) -> SecretStr | None:
    if settings.database_url is not None:
        return settings.database_url
    if os.getenv(REQUIRE_DATABASE_TESTS) == "1":
        raise RuntimeError(
            "PostgreSQL isolation proof requires DATABASE_URL when "
            "REQUIRE_DATABASE_TESTS=1. Configure the CI PostgreSQL service "
            "(.github/workflows/ci.yml)."
        )
    return None


def test_membership_repository_isolates_tenants_in_postgresql() -> None:
    database_url = isolation_database_url(integration_settings())
    if database_url is None:
        pytest.skip("DATABASE_URL is required for PostgreSQL isolation proof.")

    asyncio.run(
        prove_tenant_isolation(
            database_url.get_secret_value(),
        )
    )


def test_required_database_proof_rejects_missing_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(REQUIRE_DATABASE_TESTS, "1")

    with pytest.raises(
        RuntimeError,
        match=r"requires DATABASE_URL.*\.github/workflows/ci\.yml",
    ):
        isolation_database_url(Settings(database_url=None, _env_file=None))


async def prove_tenant_isolation(database_url: str) -> None:
    database = DatabaseManager(database_url)
    try:
        async with database.session() as session:
            tenant_a = Tenant(name=f"Isolation tenant A {uuid4()}")
            tenant_b = Tenant(name=f"Isolation tenant B {uuid4()}")
            admin_user = AdminUser(
                email=f"isolation-{uuid4()}@example.test",
                password_hash="not-a-real-password-hash",
            )
            session.add_all([tenant_a, tenant_b, admin_user])
            await session.flush()

            membership_b = TenantMembership(
                tenant_id=tenant_b.id,
                admin_user_id=admin_user.id,
                role=TenantRole.TENANT_STAFF,
            )
            session.add(membership_b)
            await session.flush()

            tenant_a_result = await TenantMembershipRepository(
                session,
                TenantContext(tenant_id=tenant_a.id),
            ).get_for_admin_user(admin_user.id)
            tenant_b_result = await TenantMembershipRepository(
                session,
                TenantContext(tenant_id=tenant_b.id),
            ).get_for_admin_user(admin_user.id)

            assert tenant_a_result is None
            assert tenant_b_result is membership_b

            await session.rollback()
    finally:
        await database.dispose()
