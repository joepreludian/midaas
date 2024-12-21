from typing import List, Dict, Union

from asaaspy.schemas.v3.my_account import MyAccountCloseViewSchema
from fastapi import APIRouter, Depends
from auth import ensure_admin_account
from asaaspy.schemas.v3.subaccount import SubAccountSchema
from schemas.account import AccountSchema, AccountDetailSchema
from services.account import inject_account_service, AccountService
import logging


logger = logging.getLogger(__name__)


router = APIRouter(tags=["Admin"], dependencies=[Depends(ensure_admin_account)])


@router.get("/{id}/")
async def get_account_detail(
    id: str,
    full: bool = False,
    account_service: AccountService = Depends(inject_account_service),
) -> Union[Dict, AccountDetailSchema]:
    """
    Get account details, getting information about the registration
    """
    if full:
        return account_service.get_by_id_extended(id)

    return AccountDetailSchema.build(account_service.get_by_id_extended(id))


@router.delete("/{id}/")
async def terminate_account(
    id: str, account_service: AccountService = Depends(inject_account_service)
) -> MyAccountCloseViewSchema:
    return account_service.terminate(id)


@router.get("/")
async def get_accounts(
    account_service: AccountService = Depends(AccountService),
) -> List[AccountSchema]:
    """
    Get all accounts registered
    """
    return account_service.all()


@router.post("/")
async def new_account(
    sub_account_data: SubAccountSchema,
    account_service: AccountService = Depends(inject_account_service),
) -> AccountSchema:
    """
    Create a new account
    """

    """
    sub_account_data.webhooks = [
        WebhookSchema(
            name=f"Midaas Webhook #{sub_account_data.name}",
            url=f"{base_config.midaas_base_url}/webhooks/{sub_account_data.cpfCnpj}",
            email=base_config.midaas_webhook_email,
            enabled=True,
            interrupted=False,
            events=[
                "TRANSFER_CREATED",
                "TRANSFER_PENDING",
                "TRANSFER_IN_BANK_PROCESSING",
                "TRANSFER_DONE",
                "TRANSFER_FAILED",
                "TRANSFER_CANCELLED",
                "BILL_CREATED",
                "BILL_PENDING",
                "BILL_BANK_PROCESSING",
                "BILL_PAID",
                "BILL_CANCELLED",
                "BILL_FAILED",
                "BILL_REFUNDED",
                "ACCOUNT_STATUS_BANK_ACCOUNT_INFO_APPROVED",
                "ACCOUNT_STATUS_BANK_ACCOUNT_INFO_AWAITING_APPROVAL",
                "ACCOUNT_STATUS_BANK_ACCOUNT_INFO_PENDING",
                "ACCOUNT_STATUS_BANK_ACCOUNT_INFO_REJECTED",
                "ACCOUNT_STATUS_COMMERCIAL_INFO_APPROVED",
                "ACCOUNT_STATUS_COMMERCIAL_INFO_AWAITING_APPROVAL",
                "ACCOUNT_STATUS_COMMERCIAL_INFO_PENDING",
                "ACCOUNT_STATUS_COMMERCIAL_INFO_REJECTED",
                "ACCOUNT_STATUS_DOCUMENT_APPROVED",
                "ACCOUNT_STATUS_DOCUMENT_AWAITING_APPROVAL",
                "ACCOUNT_STATUS_DOCUMENT_PENDING",
                "ACCOUNT_STATUS_DOCUMENT_REJECTED",
                "ACCOUNT_STATUS_GENERAL_APPROVAL_APPROVED",
                "ACCOUNT_STATUS_GENERAL_APPROVAL_AWAITING_APPROVAL",
                "ACCOUNT_STATUS_GENERAL_APPROVAL_PENDING",
                "ACCOUNT_STATUS_GENERAL_APPROVAL_REJECTED",
            ],
        )
    ]
    """
    return account_service.create(sub_account_data)
