from typing import Literal
from pydantic import BaseModel, Field


class AdminStatus(BaseModel):
    status: Literal["running", "maintenance"] = Field(default="running")
    is_maintenance: bool = Field(default=False)
    sub_accounts: int = Field(default=0)
    version: str = Field(default="VERSION_NOT_SET")


class AccountCredentialRequestSchema(BaseModel):
    account_id: str = Field()


class TokenSchema(BaseModel):
    token: str
