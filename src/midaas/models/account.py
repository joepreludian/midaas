import uuid

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, JSONAttribute
from config import BaseConfig
from schemas.account import AccountSchema

config = BaseConfig()


def _build_id():
    return str(uuid.uuid4())


class BankAccount(Model):
    class Meta:
        table_name = "accounts"
        region = config.aws_region
        host = config.aws_endpoint
        write_capacity_units = 2
        read_capacity_units = 2

    id = UnicodeAttribute(hash_key=True, default=_build_id)
    active = BooleanAttribute(default=True)
    external_id = UnicodeAttribute()
    api_key = UnicodeAttribute()
    wallet_id = UnicodeAttribute()
    payload = JSONAttribute(null=True)

    def as_account_schema(self) -> AccountSchema:
        return AccountSchema(
            **{
                **self.attribute_values,
                "name": self.payload.get("name"),
                "agency": self.payload.get("accountNumber", {}).get("agency"),
                "account": self.payload.get("accountNumber", {}).get("account"),
                "account_digit": self.payload.get("accountNumber", {}).get(
                    "accountDigit"
                ),
            }
        )
