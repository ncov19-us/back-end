from starlette.responses import JSONResponse
from fastapi import Request

from api.config import DataReadingError, DataValidationError


async def data_reading_exception_handler(
                request: Request,
                exc: DataReadingError,
            ) -> JSONResponse:

    return JSONResponse(
        status_code=422,
        content={"message": f"[ERROR] {request} -- {exc.name}"},
    )


async def data_validation_exception_handler(
                request: Request,
                exc: DataValidationError,
            ) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"message": f"[ERROR] {request} -- {exc.name}"},
    )
