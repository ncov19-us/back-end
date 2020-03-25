from fastapi import Depends, FastAPI, Header, HTTPException
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import api.endpoints
from api.config import get_logger

_logger = get_logger(logger_name=__name__)


def create_app(*, config_object) -> FastAPI:
    """
    Creates a FastAPI app to be used by ../run.py
    """
    _logger.info(f"[INFO]: Endpoint Version ")
    _logger.info(f"[INFO]: config_object is {config_object}")
    config = dict(
        {
            "title": "COID19 US API",
            "description": "Initial release of COID19 US API",
            "version": "0.0",
        }
    )

    app = FastAPI(
        title=config["title"],  # "COVID19 US API",
        description=config["description"],  #: "Initial release of COVID19 US API",
        version=config["version"],
    )  #: api.__version__)#config)

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

    _logger.info("FastAPI instance created")

    return app
