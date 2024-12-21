from fastapi import APIRouter, Depends
from auth import ensure_client_account, ClientReturn
from asaaspy.schemas.v3.bank import BankBalanceViewSchema

router = APIRouter(tags=["banking"], dependencies=[Depends(ensure_client_account)])


@router.get("/me/")
async def get_me():
    return {"message": "Welcome to the banking API!"}


@router.get("/balance/")
async def get_balance(user_data: ClientReturn = Depends(ensure_client_account)) -> BankBalanceViewSchema:
    return user_data.asaas.bank.get_balance()