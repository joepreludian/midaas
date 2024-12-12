from typing import List, Optional
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
