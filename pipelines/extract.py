import json
import requests
from utils.logger import get_logger
from utils.config import WEATHER_API_URL, WEATHER_PARAMS, RAW_DATA_PATH

logger = get_logger(__name__)

def extract():
    logger.info(f"Requesting weather data from {WEATHER_API_URL}")
    logger.info(f"Using params: {WEATHER_PARAMS}")

    response = requests.get(WEATHER_API_URL, params=WEATHER_PARAMS, timeout=30)

    if response.status_code != 200:
        logger.error(f"API error: {response.status_code} - {response.text}")
        raise Exception(f"Weather API request failed with {response.status_code}")

    data = response.json()

    # Save raw JSON
    with open(RAW_DATA_PATH, "w") as f:
        json.dump(data, f)

    logger.info(f"Saved raw weather data to {RAW_DATA_PATH}")
    return data
