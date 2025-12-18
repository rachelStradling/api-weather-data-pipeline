import pandas as pd
from utils.logger import get_logger
from utils.config import HISTORICAL_OUTPUT_CSV_PATH
from pipelines.load_bigquery import load_to_bigquery

logger = get_logger(__name__)

def main():
    logger.info(f"Reading historical CSV: {HISTORICAL_OUTPUT_CSV_PATH}")
    df = pd.read_csv(HISTORICAL_OUTPUT_CSV_PATH)

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    load_to_bigquery(df)

if __name__ == "__main__":
    main()
