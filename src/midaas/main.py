from fastapi import FastAPI
from routers.admin import router as admin_router
from routers.banking import router as banking_router
from routers.accounts import router as accounts_router
from routers.withdraw import router as withdraw_router
from config import base_config
from middleware import ErrorGuardHandlerMiddleware

app = FastAPI(title="Midaas", description="Small Bank as a service interface")

# Adding Routers
app.include_router(admin_router, prefix="/admin")
app.include_router(accounts_router, prefix="/accounts")
app.include_router(banking_router, prefix="/banking")
app.include_router(withdraw_router, prefix="/withdraw")

# Add Middlewares
if not base_config.dev_environment:
    app.add_middleware(ErrorGuardHandlerMiddleware)
