from fastapi import APIRouter, Depends
from uuid import UUID

from auth import ensure_admin_account
from models.account import BankAccount

import logging

from schemas.admin import AccountCredentialRequestSchema, TokenSchema
from services.account import AccountService
from services.auth import inject_auth_service, AuthService

logger = logging.getLogger(__name__)


router = APIRouter(tags=["Admin"], dependencies=[Depends(ensure_admin_account)])





@router.post("/build_token/")
async def issue_access_token(data: AccountCredentialRequestSchema, auth_svc: AuthService = Depends(inject_auth_service)) -> TokenSchema:
    """
    Given a sub_account id, generate a new JWT access token.
    It will have an expiration date. Time to time this method must be called.
    """
    return auth_svc.build_token(data.account_id)


@router.get("/setup/")
async def setup_database():
    """
    Given AWS Account set up, create a DynamoDB table to handle accounts
    """
    BankAccount.create_table(read_capacity_units=2, write_capacity_units=2, wait=True)
    return {"status": "Successful"}
