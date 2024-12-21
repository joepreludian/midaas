from typing import Optional

from pydantic import Field

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    dev_environment: bool = Field(default=False)

    asaas_key: str = Field()
    asaas_sandbox: bool = Field()

    aws_region: str = Field(default="us-east-1")
    aws_access_key_id: str = Field(default="<KEY>")
    aws_secret_access_key: str = Field(default="<KEY>")
    aws_endpoint: Optional[str] = Field(default=None)

    midaas_admin_token: str = Field()
    midaas_webhook_email: str = Field()
    midaas_jwt_secret: str = Field()
    midaas_base_url: str = Field(default="http://localhost:9999")
    midaas_user_token_time_minutes: int = Field(default=30)


base_config = BaseConfig()
