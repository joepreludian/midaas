from fastapi import FastAPI
from routers.admin import router as admin_router
from routers.accounts import router as accounts_router
from config import base_config
from middleware import ErrorGuardHandlerMiddleware

app = FastAPI(title="Midaas", description="Small Bank as a service interface")

# Adding Routers
app.include_router(admin_router, prefix="/admin")
app.include_router(accounts_router, prefix="/accounts")

# Add Middlewares
if not base_config.dev_environment:
    app.add_middleware(ErrorGuardHandlerMiddleware)
