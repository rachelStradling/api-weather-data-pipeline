import pandas as pd
from utils.logger import get_logger
from utils.config import FORECAST_OUTPUT_CSV_PATH,BQ_PROJECT_ID,BQ_DATASET_ID,BQ_TABLE_HOURLY_FORECAST
from pipelines.load_bigquery import load_to_bigquery

logger = get_logger(__name__)

def main():
    logger.info(f"Reading forecast CSV: {FORECAST_OUTPUT_CSV_PATH}")
    df = pd.read_csv(FORECAST_OUTPUT_CSV_PATH)

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    load_to_bigquery(df,f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_HOURLY_FORECAST}")

if __name__ == "__main__":
    main()
