from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import base_config

security = HTTPBearer()


def ensure_admin_account(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    if credentials.credentials == base_config.midaas_admin_token:
        return {"scheme": credentials.scheme, "credentials": credentials.credentials}

    raise HTTPException(status_code=401, detail="Invalid Credentials")
