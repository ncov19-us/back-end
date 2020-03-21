from fastapi import Depends, FastAPI, Header, HTTPException
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api import endpoints
from api.config import get_logger


_logger = get_logger(logger_name=__name__)


def create_app(*, config_object) -> FastAPI:
    """
    Creates a FastAPI app to be used by ../run.py
    """
    _logger.info(f"[INFO]: Endpoint Version {api.__version__}")
    _logger.info(f"[INFO]: config_object is {config_object}")
    config = dict(
        {
            "title": "Memefly API",
            "description": "Initial release of Memefly API",
            "version": api.__version__,
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
