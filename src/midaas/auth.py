from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import base_config
from services.auth import inject_auth_service, AuthService
from models.account import BankAccount
from asaaspy.service import AsaasService
from dataclasses import dataclass
from jose.exceptions import ExpiredSignatureError

security = HTTPBearer()

@dataclass()
class ClientReturn:
    asaas: AsaasService
    account: BankAccount


def ensure_admin_account(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    if credentials.credentials == base_config.midaas_admin_token:
        return {"scheme": credentials.scheme, "credentials": credentials.credentials}

    raise HTTPException(status_code=401, detail="Token is invalid")


async def ensure_client_account(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_svc: AuthService = Depends(inject_auth_service)
) -> ClientReturn:
    try:
        returned_account = auth_svc.get_account(credentials.credentials)
    except ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Token expired")

    client_asaas = AsaasService(
        api_key=returned_account.api_key, sandbox=base_config.asaas_sandbox
    )

    if not returned_account:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return ClientReturn(asaas=client_asaas, account=returned_account)
