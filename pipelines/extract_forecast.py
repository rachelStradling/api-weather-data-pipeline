import json
import os
import requests

from utils.logger import get_logger
from utils.config import FORECAST_API_URL, CITIES, HOURLY_VARIABLES, DAILY_VARIABLES, RAW_DATA_DIR

logger = get_logger(__name__)

def extract_forecast(city_name : str, forecast_days : int):
    """
    Extract forecast weather data for a single city between now and the next
    forecast_days number of days. Max(forecast_days) = 16
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
        "forecast_days": forecast_days,
    }

    logger.info(f"[forecast] Requesting {city_name} {forecast_days}-day forecast")

    response = requests.get(FORECAST_API_URL, params=params)

    if response.status_code == 200:
            data = response.json()

            forecast_dir = os.path.join(RAW_DATA_DIR, "forecast")
            os.makedirs(forecast_dir, exist_ok=True)
            raw_path = os.path.join(forecast_dir, f"weather_forecast_{city_name}_{forecast_days}-days.json")
            with open(raw_path, "w") as f:
                json.dump(data, f)

            logger.info(f"[forecast] Saved raw data to {raw_path}")
            return data

    if response.status_code != 200:
        logger.error(
            f"[forecast] API error for {city_name}: {response.status_code} - {response.text}"
        )
        raise Exception(f"Forecast API request failed for {city_name} with {response.status_code}")
        
