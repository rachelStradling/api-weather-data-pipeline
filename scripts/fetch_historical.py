import argparse
import pandas as pd

from pipelines.extract_historical import extract_historical
from pipelines.transform import transform
from pipelines.load import load
from utils.logger import get_logger
from utils.config import CITIES, HISTORICAL_OUTPUT_CSV_PATH,ARCHIVE_START_DATE,ARCHIVE_END_DATE

logger = get_logger(__name__)

def run_historical(start_date: str, end_date: str):
    logger.info(f"Starting historical run: {start_date} → {end_date}")

    dfs = []
    for city_name in CITIES.keys():
        raw = extract_historical(city_name, start_date, end_date)
        df = transform(raw, city_name)
        dfs.append(df)

    full_df = pd.concat(dfs, ignore_index=True)

    # Save to a separate historical CSV (don’t overwrite forecast output)
    full_df.to_csv(HISTORICAL_OUTPUT_CSV_PATH, index=False)
    logger.info(f"Saved historical hourly data to {HISTORICAL_OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", help="YYYY-MM-DD")
    parser.add_argument("--end-date", help="YYYY-MM-DD")
    args = parser.parse_args()

    # Use CLI arguments if provided, otherwise fall back to config defaults
    start_date = args.start_date or ARCHIVE_START_DATE
    end_date = args.end_date or ARCHIVE_END_DATE

    run_historical(start_date, end_date)
