import time
import json
import os
import requests

from utils.logger import get_logger
from utils.config import ARCHIVE_API_URL, CITIES, HOURLY_VARIABLES, DAILY_VARIABLES, RAW_DATA_DIR

logger = get_logger(__name__)

MAX_RETRIES = 5
RETRY_SLEEP_SECONDS = 60  # wait 1 min on 429

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

    for attempt in range(1, MAX_RETRIES + 1):
        
        response = requests.get(ARCHIVE_API_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            historical_dir = os.path.join(RAW_DATA_DIR, "historical")
            os.makedirs(historical_dir, exist_ok=True)
            raw_path = os.path.join(historical_dir, f"weather_archive_{city_name}_{start_date}_{end_date}.json")
            with open(raw_path, "w") as f:
                json.dump(data, f)

            logger.info(f"[archive] Saved raw data to {raw_path}")
            return data

        if response.status_code == 429:
            logger.error(
                f"[archive] API rate limit for {city_name}: 429. "
                f"Attempt {attempt}/{MAX_RETRIES}. Waiting {RETRY_SLEEP_SECONDS} seconds..."
            )
            time.sleep(RETRY_SLEEP_SECONDS)
            continue  # try again

        # other errors
        logger.error(
            f"[archive] API error for {city_name}: {response.status_code} - {response.text}"
        )
        raise Exception(f"Archive API request failed for {city_name} with {response.status_code}")


    # if we get here, all retries failed with 429
    raise Exception(f"Archive API request failed for {city_name} after {MAX_RETRIES} retries (rate limited)")
