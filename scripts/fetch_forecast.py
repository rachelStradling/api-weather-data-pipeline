import argparse
import pandas as pd

from pipelines.extract_forecast import extract_forecast
from pipelines.transform import transform
from utils.logger import get_logger
from utils.config import CITIES, FORECAST_OUTPUT_CSV_PATH,FORECAST_DAYS

logger = get_logger(__name__)

def run_forecast(forecast_days: int):
    logger.info(f"Starting forecast run: {forecast_days} days ahead")

    dfs = []
    for city_name in CITIES.keys():
        raw = extract_forecast(city_name, forecast_days)
        df = transform(raw, city_name)
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)

    # Save to a forecast CSV
    full_df.to_csv(FORECAST_OUTPUT_CSV_PATH, index=False)
    logger.info(f"Saved forecast hourly data to {FORECAST_OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--forecast-days", help="int")
    args = parser.parse_args()

    # Use CLI arguments if provided, otherwise fall back to config default
    forecast_days = args.forecast_days or FORECAST_DAYS

    run_forecast(forecast_days)
