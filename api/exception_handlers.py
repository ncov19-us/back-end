from starlette.responses import JSONResponse
from fastapi import Request

from api.config import DataReadingError, DataValidationError


async def data_reading_exception_handler(
                request: Request,
                exc: DataReadingError,
            ) -> JSONResponse:

    return JSONResponse(
        status_code=422,
        content={"message": f"[ERROR] {request.method} -- {exc}"},
    )


async def data_validation_exception_handler(
                request: Request,
                exc: DataValidationError,
            ) -> JSONResponse:
    # this will hang, so just print out method directly for info
    # body = await request.body()
    return JSONResponse(
        status_code=422,
        content={"message": f"[ERROR] {request.method} -- {exc}"},
    )
