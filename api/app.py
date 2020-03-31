import uvicorn
from fastapi import FastAPI
from fastapi import Depends, FastAPI, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware

import api
import api.endpoints
from api.config import get_logger
from api.config import Config

_logger = get_logger(logger_name=__name__)


def create_app(*, config_object) -> FastAPI:
    """Creates a FastAPI app.

    :param: :Config: config_object. app config.
    """
    _logger.info(f"[INFO]: Endpoint Version ")
    _logger.info(f"[INFO]: config_object is {config_object}")
    config = dict(
        {
            "title": "ncov19.us API",
            "version": f"{api.__version__}",
            "description": """API Support: ncov19us@gmail.com | URL: https://github.com/ncov19-us/back-end | [GNU GENERAL PUBLIC LICENSE](https://github.com/ncov19-us/back-end/blob/master/LICENSE)""",
        }
    )

    app = FastAPI(
        title=config["title"],
        version=config["version"],
        description=config["description"],
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

    _logger.info("FastAPI instance created")

    return app
