from fastapi import APIRouter, Depends
from auth import ensure_admin_account
from models.account import BankAccount

import logging


logger = logging.getLogger(__name__)


router = APIRouter(tags=["Admin"], dependencies=[Depends(ensure_admin_account)])


@router.get("/status/")
async def get_project_status(): ...


@router.get("/database_setup/")
async def setup_database():
    BankAccount.create_table(read_capacity_units=2, write_capacity_units=2, wait=True)
    return {"msg": "Successful"}
