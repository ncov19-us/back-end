import os
from fastapi import APIRouter
from pydantic import BaseModel
from api.config import DevelopmentConfig as dev_config
from api.config import ProductionConfig as prod_config
from api.utils.twitter_mongo import TwitterMongo
import api

# Starts the FastAPI Router to be used by the FastAPI app.
router = APIRouter()


@router.get("/")
def root():
    """
    Root URL, for version checking.
    """
    return f"COVID19 US Data API, Model {api.__version__}"
