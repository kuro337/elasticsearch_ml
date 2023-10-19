from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from server.utils.logger import init_logger
from settings.constants import module_name

logger = init_logger(module_name)


async def universal_exception_handler(request: Request, exc: Exception):
    logger.error(
        f"An error occurred: {exc}", exc_info=True
    )  # Logs the error with traceback
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": "Internal Server Error"}),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        f"HTTP exception occurred: {exc.detail}", exc_info=True
    )  # Logs the error with traceback
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail}),
    )
