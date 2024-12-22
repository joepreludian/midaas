from pydantic import BaseModel
from typing import Literal


class WithdrawAccount(BaseModel):
    pix_key: str
    pix_type: Literal["CPF", "CNPJ", "EMAIL", "PHONE", "EVP"]
