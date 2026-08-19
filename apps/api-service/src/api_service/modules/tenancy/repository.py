from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_service.modules.tenancy.context import TenantContext
from api_service.modules.tenancy.models import TenantMembership

TENANT_CONTEXT_REQUIRED = (
    "Tenant-scoped repositories require TenantContext "
    "(docs/product/tenancy.md). Derive it from an authenticated session "
    "or verified bot identity."
)


class TenantScopedRepository:
    def __init__(self, session: AsyncSession, context: TenantContext) -> None:
        if not isinstance(context, TenantContext):
            raise TypeError(TENANT_CONTEXT_REQUIRED)
        self._session = session
        self._context = context


class TenantMembershipRepository(TenantScopedRepository):
    def statement_for_admin_user(self, admin_user_id: UUID) -> Select:
        return select(TenantMembership).where(
            TenantMembership.tenant_id == self._context.tenant_id,
            TenantMembership.admin_user_id == admin_user_id,
        )

    async def get_for_admin_user(
        self,
        admin_user_id: UUID,
    ) -> TenantMembership | None:
        result = await self._session.execute(
            self.statement_for_admin_user(admin_user_id),
        )
        return result.scalar_one_or_none()
