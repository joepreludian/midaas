from datetime import datetime, timedelta, UTC
from functools import lru_cache

from jose import jwt
from uuid import UUID
from midaas.config import base_config
from midaas.models.account import BankAccount
from schemas.admin import TokenSchema
from midaas.config import base_config



class AuthService:
    def __init__(self):
        self._jwt_secret = base_config.midaas_jwt_secret
        self._jwt_algorithm = "HS256"

    def build_token(self, account_id: str) -> TokenSchema:
        account = BankAccount.get(account_id)
        expiration_date = datetime.now(UTC) + timedelta(minutes=base_config.midaas_user_token_time_minutes)

        jwt_token_body = {
            "exp": expiration_date.timestamp(),
            "id": account.id,
        }

        jwt_token = jwt.encode(jwt_token_body, self._jwt_secret, algorithm=self._jwt_algorithm)
        return TokenSchema(token=jwt_token)

    def get_account(self, jwt_token: str) -> BankAccount:
        decoded_data = jwt.decode(jwt_token, self._jwt_secret, algorithms=self._jwt_algorithm)
        account = BankAccount.get(decoded_data["id"])

        # @TODO update project in order to return None (check)
        return account


@lru_cache
def inject_auth_service():
    return AuthService()
