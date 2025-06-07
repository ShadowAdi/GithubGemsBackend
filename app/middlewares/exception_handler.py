from fastapi import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config import logger


async def global_exception_handler(req: Request, exc: Exception):
    logger.error(f"Internal Server Error Occurred {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An Internal Server Error Occurred.",
            "detail": str(exc),
        },
    )


async def http_execution_handler(req: Request, exc: StarletteHTTPException):
    logger.error(f"{exc.detail}")
    return JSONResponse(
        status_code=exc.status_code, content={"success": False, "message": exc.detail}
    )


async def validation_exception_handler(req: Request, exc: RequestValidationError):
    logger.error(f"Validation Failed {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed.",
            "errors": exc.errors(),
        },
    )
