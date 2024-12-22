from fastapi import FastAPI
from routers.admin import router as admin_router
from routers.banking import router as banking_router
from routers.accounts import router as accounts_router
from routers.withdraw import router as withdraw_router
from routers.main import router as main_router
from middleware import ErrorGuardHandlerMiddleware

app = FastAPI(title="Midaas", description="Small Bank as a service interface")

# Adding Routers /v1
app.include_router(main_router)
app.include_router(admin_router, prefix="/v1/admin")
app.include_router(accounts_router, prefix="/v1/accounts")
app.include_router(banking_router, prefix="/v1/banking")
app.include_router(withdraw_router, prefix="/v1/withdraw_account")

# Add Middlewares
app.add_middleware(ErrorGuardHandlerMiddleware)
