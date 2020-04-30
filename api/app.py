from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import api
import api.endpoints
from api.exception_handlers import data_reading_exception_handler
from api.exception_handlers import data_validation_exception_handler
from api.config import get_logger
from api.config import app_config
from api.config import DataReadingError, DataValidationError


_logger = get_logger(logger_name=__name__)


def create_app() -> FastAPI:
    """Creates a FastAPI app.

    :param: :Config: config_object. app config.
    """
    _logger.info(f"[INFO]: Endpoint Version {api.__version__}")
    _logger.info(f"[INFO]: config_object is {app_config}")

    app = FastAPI(
        title=app_config.INFO["title"],
        version=api.__version__,
        description=app_config.INFO["description"],
    )

    # All the API Routers are stored in endpoints.py, so we import them
    # to the app here.
    app.include_router(api.endpoints.router)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(DataReadingError, data_reading_exception_handler)
    app.add_exception_handler(
        DataValidationError, data_validation_exception_handler
    )

    _logger.info("FastAPI instance created")

    return app
