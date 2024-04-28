import os
from typing import Any, Dict

import json
from dotenv import load_dotenv
from passlib.context import CryptContext

from yookassa import Configuration

load_dotenv()

VOTE_PRICE = 100
DESCRIPTION = "Покупка голосов"
HOST = "https://bitracking.ru"

METRICS = os.environ.get("METRICS", "") == "true"

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

PRODUCTION = os.environ.get("PRODUCTION") == "true"

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# S3
MINIO_ADDRESS = os.environ.get("MINIO_ADDRESS")
S3_WORKER_API = os.environ.get("S3_WORKER_API")
BUCKET_NAME = "bitracking_bucket"

# YOOKASSA
YOOKASSA_ACCOUNT_ID = os.environ.get("YOOKASSA_ACCOUNT_ID", None)
YOOKASSA_SECRET_KEY = os.environ.get("YOOKASSA_SECRET_KEY", None)
Configuration.account_id = YOOKASSA_ACCOUNT_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY

# REGIONS
with open("russia.json", mode="r", encoding="UTF-8") as file:
    ALL_DATA = json.load(file)["data"]
ALL_REGIONS = {}
DISTRICTS_WITH_AREA = {}
for district in ALL_DATA:
    for area in district["areas"]:
        ALL_REGIONS[area["name"]] = 0
        if not DISTRICTS_WITH_AREA.get(district["name"]):
            DISTRICTS_WITH_AREA[district["name"]] = []
        DISTRICTS_WITH_AREA[district["name"]].append(area["name"])
REGIONS_IN_ONE_STAGE_WINNERS = []

# LOGGING
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s | %(name)s | %(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s | %(name)s | %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            # noqa: E501
        },
        "my_formatter": {
            "()": "logging.Formatter",
            "fmt": "%(asctime)s | %(name)s | %(levelname)-8s | [%(pathname)s:%(lineno)d] | %(message)s",
        },
    },
    "handlers": {
        "my_handler": {
            "formatter": "my_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "app": {"handlers": ["my_handler"], "level": "DEBUG", "propagate": False},
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
