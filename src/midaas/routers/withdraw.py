from fastapi import APIRouter, Depends, HTTPException
from auth import ClientReturn, ensure_client_account
from typing import Optional

import logging

from schemas.banking import WithdrawAccount

logger = logging.getLogger(__name__)


router = APIRouter(tags=["Withdraw"], dependencies=[Depends(ensure_client_account)])


@router.get("/get/")
async def get_withdraw_account(user_data: ClientReturn = Depends(ensure_client_account)) -> WithdrawAccount:
    if result := user_data.account.get_withdraw_account():
        return result

    raise HTTPException(status_code=404)

@router.post("/set/")
async def set_withdraw_account(withdraw_request: WithdrawAccount, user_data: ClientReturn = Depends(ensure_client_account)) -> WithdrawAccount:
    user_data.account.withdraw_account = withdraw_request.model_dump()
    user_data.account.save()

    return user_data.account.get_withdraw_account()