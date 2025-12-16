import json
import os
import requests

from utils.logger import get_logger
from utils.config import ARCHIVE_API_URL, CITIES, HOURLY_VARIABLES, DAILY_VARIABLES, RAW_DATA_DIR

logger = get_logger(__name__)

def extract_historical(city_name: str, start_date: str, end_date: str):
    """
    Extract historical weather data for a single city between start_date and end_date.
    Dates must be YYYY-MM-DD.
    """
    if city_name not in CITIES:
        raise ValueError(f"City '{city_name}' not found in CITIES config")

    city_cfg = CITIES[city_name]

    params = {
        "latitude": city_cfg["latitude"],
        "longitude": city_cfg["longitude"],
        "hourly": HOURLY_VARIABLES,
        "daily": DAILY_VARIABLES,      # sunrise/sunset
        "timezone": city_cfg["timezone"],
        "start_date": start_date,
        "end_date": end_date,
    }

    logger.info(f"[archive] Requesting {city_name} from {start_date} to {end_date}")
    response = requests.get(ARCHIVE_API_URL, params=params, timeout=60)

    if response.status_code != 200:
        logger.error(f"[archive] API error for {city_name}: {response.status_code} - {response.text}")
        raise Exception(f"Archive API request failed for {city_name} with {response.status_code}")

    data = response.json()

    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    raw_path = os.path.join(RAW_DATA_DIR, f"weather_archive_{city_name}_{start_date}_{end_date}.json")
    with open(raw_path, "w") as f:
        json.dump(data, f)

    logger.info(f"[archive] Saved raw data to {raw_path}")
    return data
