from asaaspy.schemas.v3.transfer import TransferSchema, TransferItemViewSchema
from fastapi import APIRouter, Depends, HTTPException
from auth import ensure_client_account, ClientReturn
from asaaspy.schemas.v3.bank import BankBalanceViewSchema, TransactionItemViewSchema

from typing import List
from schemas.account import AccountDetailSchema
from schemas.banking import WithdrawPayload
from services.account import AccountService, inject_account_service

router = APIRouter(tags=["banking"], dependencies=[Depends(ensure_client_account)])


@router.get("/me/")
async def get_me(
    user_data: ClientReturn = Depends(ensure_client_account),
    account_service: AccountService = Depends(inject_account_service),
):
    """
    Get information about a user. Should have a Bearer token that came from /v1/admin/build_token/
    """
    return AccountDetailSchema.build(
        account_service.get_by_id_extended(user_data.account.id)
    )


@router.get("/balance/")
async def get_balance(
    user_data: ClientReturn = Depends(ensure_client_account),
) -> BankBalanceViewSchema:
    """
    Get the available funds of the user account
    """
    return user_data.asaas.bank.get_balance()


@router.get("/transactions/")
async def get_transactions(
    user_data: ClientReturn = Depends(ensure_client_account),
) -> List[TransactionItemViewSchema]:
    """Return a list of available transactions"""
    return user_data.asaas.bank.get_transactions(limit=100)


@router.post("/withdraw/")
async def withdraw_value(
    data: WithdrawPayload, user_data: ClientReturn = Depends(ensure_client_account)
) -> TransferItemViewSchema:
    withdraw_account = user_data.account.get_withdraw_account()

    if not withdraw_account:
        raise HTTPException(status_code=400, detail="No withdraw account found")

    result = user_data.asaas.transfer.create(
        TransferSchema(
            value=data.value,
            pixAddressKey=withdraw_account.pix_key,
            pixAddressKeyType=withdraw_account.pix_type,
            description="Transferencia de fundos",
        )
    )

    return result
