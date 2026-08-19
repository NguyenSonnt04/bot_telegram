import asyncio
from uuid import uuid4

import pytest

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


def test_membership_repository_isolates_tenants_in_postgresql() -> None:
    settings = Settings()
    if settings.database_url is None:
        pytest.skip("DATABASE_URL is required for PostgreSQL isolation proof.")

    asyncio.run(
        prove_tenant_isolation(
            settings.database_url.get_secret_value(),
        )
    )


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
