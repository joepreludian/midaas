from fastapi import APIRouter, Depends
from uuid import UUID

from auth import ensure_admin_account
from models.account import BankAccount

import logging

from schemas.admin import AccountCredentialRequestSchema, TokenSchema
from services.auth import inject_auth_service, AuthService

logger = logging.getLogger(__name__)


router = APIRouter(tags=["Admin"], dependencies=[Depends(ensure_admin_account)])


@router.get("/status/")
async def get_project_status(): ...


@router.post("/build_token/")
async def issue_access_token(data: AccountCredentialRequestSchema, auth_svc: AuthService = Depends(inject_auth_service)) -> TokenSchema:
    return auth_svc.build_token(data.account_id)


@router.get("/setup/")
async def setup_database():
    BankAccount.create_table(read_capacity_units=2, write_capacity_units=2, wait=True)
    return {"status": "Successful"}
