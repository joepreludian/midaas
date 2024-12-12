from asaaspy.exceptions import AsaasClientError
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class ErrorGuardHandlerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except AsaasClientError as e:
            response = JSONResponse(status_code=422, content={"error": e.details})
            await response(scope, receive, send)
        except Exception as e:
            response = JSONResponse(status_code=422, content={"error": str(e)})
            await response(scope, receive, send)
