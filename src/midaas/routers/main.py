from fastapi import APIRouter, Depends

from schemas.account import HealthStatusSchema
from services.account import AccountService, inject_account_service

router = APIRouter()


@router.get("/health/", responses={200: {"model": HealthStatusSchema}, 218: {"model": HealthStatusSchema, "description": "This Is Fine: Unhealthy System. Will show you the remarks about what went wrong"}})
async def get_project_status(
        account_service: AccountService = Depends(inject_account_service)) -> HealthStatusSchema:

    return account_service.get_admin_status()
