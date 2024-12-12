from fastapi import APIRouter, Depends
from auth import ensure_admin_account

import logging


logger = logging.getLogger(__name__)


router = APIRouter(tags=["Webhook"], dependencies=[Depends(ensure_admin_account)])


@router.get("/webhook_handler/{account_id}")
async def handle_webhook(account_id: str): ...
