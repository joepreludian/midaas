from typing import List, Optional, Literal

from asaaspy.schemas.v3.my_account import MyAccountStatusViewSchema
from pydantic import BaseModel, Field


class AccountSchema(BaseModel):
    id: str
    wallet_id: str
    name: str
    agency: str
    account: str
    account_digit: str


class AccountFile(BaseModel):
    type: str
    title: str


class AccountDetailSchema(BaseModel):
    id: str
    is_approved: bool = Field(default=False)
    onboard_url: Optional[str] = None
    missing_documents: List[AccountFile] = Field(default=list)

    @classmethod
    def build(cls, data) -> "AccountDetailSchema":
        obj = {
            "is_approved": data["statuses"]["general"] == "APPROVED",
            "missing_documents": [
                AccountFile(**item) for item in data["documents"]["data"]
            ],
            "onboard_url": data["documents"]["data"][0]["onboardingUrl"]
            if data["documents"]["data"]
            else None,
            "id": data["id"],
        }
        return cls(**obj)


class HealthStatusSchema(BaseModel):
    status: Literal["healthy", "unhealthy"]
    sub_accounts: int
    asaas_root_account_status: Optional[MyAccountStatusViewSchema]
    remarks: List[str]
