from asaaspy.exceptions import AsaasClientError
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send
from midaas.config import base_config
from pynamodb.exceptions import DoesNotExist

class ErrorGuardHandlerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        response = None
        try:
            await self.app(scope, receive, send)

        except DoesNotExist as exc:
            response = JSONResponse(status_code=404, content={"error": str(exc)})

        except AsaasClientError as e:
            response = JSONResponse(status_code=e.status_code, content=e.details)

        except Exception as e:
            if base_config.dev_environment:
                raise e from e

            response = JSONResponse(status_code=422, content={"error": str(e)})

        finally:
            await response(scope, receive, send)