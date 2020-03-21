import os
from fastapi import APIRouter
from pydantic import BaseModel
from api.config import DevelopmentConfig as conf

VERSION = "VERSION"

with open(VERSION) as file_io:
    version = [line.rstrip() for line in file_io]


async def root():
    """
    Root URL, for version checking.
    """
    return f"REST API, Model {version[0]}"
