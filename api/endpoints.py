import os
from fastapi import APIRouter
from pydantic import BaseModel
from api.config import DevelopmentConfig as dev_config
from api.config import ProductionConfig as prod_config
from api.utils.twitter_mongo import TwitterMongo

# Starts the FastAPI Router to be used by the FastAPI app.
router = APIRouter()


@router.get("/")
def root():
    """
    Root URL, for version checking.
    """
    return f"COVID19 US Data API, Model"


# @router.get("/news/{state}")
# def get_gnews(state: str):
#     state = reverse_states_map["state"]
#     df = gnews.get_state_topic_google_news(state, "Coronavirus")

#     return gnews.convert_df_to_json(df)
