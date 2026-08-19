import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.dialects import postgresql

from api_service.modules.tenancy import (
    TenantContext,
    TenantMembershipRepository,
)
from api_service.modules.tenancy.repository import TENANT_CONTEXT_REQUIRED


def test_membership_query_uses_tenant_context() -> None:
    tenant_id = uuid4()
    admin_user_id = uuid4()
    repository = TenantMembershipRepository(
        AsyncMock(),
        TenantContext(tenant_id=tenant_id),
    )

    compiled = repository.statement_for_admin_user(admin_user_id).compile(
        dialect=postgresql.dialect(),
    )

    assert tenant_id in compiled.params.values()
    assert admin_user_id in compiled.params.values()
    assert "tenant_memberships.tenant_id =" in str(compiled)
    assert "tenant_memberships.admin_user_id =" in str(compiled)


def test_membership_repository_rejects_raw_tenant_id() -> None:
    with pytest.raises(TypeError, match="docs/product/tenancy.md"):
        TenantMembershipRepository(AsyncMock(), uuid4())  # type: ignore[arg-type]

    assert "authenticated session or verified bot identity" in TENANT_CONTEXT_REQUIRED


def test_membership_repository_returns_scoped_result() -> None:
    expected_membership = MagicMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = expected_membership
    session = AsyncMock()
    session.execute.return_value = result
    repository = TenantMembershipRepository(
        session,
        TenantContext(tenant_id=uuid4()),
    )

    membership = asyncio.run(repository.get_for_admin_user(uuid4()))

    assert membership is expected_membership
    session.execute.assert_awaited_once()
