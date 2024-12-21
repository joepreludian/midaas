from functools import lru_cache

from models.account import BankAccount
from asaaspy.schemas.v3.subaccount import SubAccountSchema
from asaaspy.service import AsaasService
from config import base_config
import logging
from typing import Optional


logger = logging.getLogger(__name__)


class AccountService:
    def __init__(self, api_key: Optional[str] = None):
        self._asaas_service = AsaasService(
            api_key=base_config.asaas_key, sandbox=base_config.asaas_sandbox
        )
        logger.info("Account Service Ready")

    def _get_asaas_account(self, id):
        account = BankAccount.get(id)
        asaas_svc_subaccount = AsaasService(
            api_key=account.api_key, sandbox=base_config.asaas_sandbox
        )

        return account, asaas_svc_subaccount

    def create(self, sub_account_request: SubAccountSchema):
        logger.info("Create Account Requested")
        account_details = self._asaas_service.sub_accounts.create(sub_account_request)
        new_account = BankAccount(
            external_id=account_details.id,
            api_key=account_details.apiKey,
            wallet_id=account_details.walletId,
            payload=account_details.model_dump(),
        )
        new_account.save()

        return new_account.as_account_schema()

    def delete(self, id):
        logger.info("Delete Account Requested")
        return self._asaas_service.sub_accounts.terminate(id)

    def all(self):
        logger.info("Getting all available accounts")
        return [item.as_account_schema() for item in BankAccount.scan()]

    def get_by_id(self, id):
        logger.info(f"Retrieve Account by ID {id}")
        item = BankAccount.get(id)
        return item.as_account_schema()

    def get_by_id_extended(self, id):
        account, asaas_svc_subaccount = self._get_asaas_account(id)
        return {
            "id": id,
            "statuses": asaas_svc_subaccount.my_account.get_status().model_dump(),
            "documents": asaas_svc_subaccount.my_account.get_pending_documents().model_dump(),
        }

    def terminate(self, id):
        logger.info(f"Delete Account by ID {id}")
        account, asaas_svc_subaccount = self._get_asaas_account(id)

        close_account_response = asaas_svc_subaccount.my_account.close_account(
            reason="Encerramento de conta"
        )
        account.delete()

        return close_account_response


@lru_cache
def inject_account_service():
    return AccountService()
