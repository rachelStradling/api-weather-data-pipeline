import json
import os
import requests
from utils.logger import get_logger
from utils.config import WEATHER_API_URL, CITIES, HOURLY_VARIABLES, DAILY_VARIABLES, RAW_DATA_DIR

logger = get_logger(__name__)

def extract(city_name: str):
    """
    Extract weather data for a single city.
    Returns the raw JSON dict from the API.
    """
    if city_name not in CITIES:
        raise ValueError(f"City '{city_name}' not found in CITIES config")

    city_cfg = CITIES[city_name]

    params = {
    "latitude": city_cfg["latitude"],
    "longitude": city_cfg["longitude"],
    "hourly": HOURLY_VARIABLES,
    "daily": DAILY_VARIABLES,
    "timezone": city_cfg["timezone"],
    }

    logger.info(f"Requesting weather for {city_name} from {WEATHER_API_URL}")
    logger.info(f"Params: {params}")

    response = requests.get(WEATHER_API_URL, params=params, timeout=30)

    if response.status_code != 200:
        logger.error(f"API error for {city_name}: {response.status_code} - {response.text}")
        raise Exception(f"Weather API request failed for {city_name} with {response.status_code}")

    data = response.json()

    # Ensure raw directory exists
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    raw_path = os.path.join(RAW_DATA_DIR, f"weather_{city_name}.json")
    with open(raw_path, "w") as f:
        json.dump(data, f)

    logger.info(f"Saved raw weather data for {city_name} to {raw_path}")
    return data
