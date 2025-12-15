import pandas as pd

from pipelines.extract import extract
from pipelines.transform import transform
from pipelines.load import load
from utils.logger import get_logger
from utils.config import CITIES

logger = get_logger(__name__)

def run_pipeline():
    logger.info("Starting multi-city weather pipeline")

    all_dfs = []

    for city_name in CITIES.keys():
        logger.info(f"Processing city: {city_name}")
        raw = extract(city_name)
        df = transform(raw, city_name)
        all_dfs.append(df)

    # Combine all cities into one DataFrame
    full_df = pd.concat(all_dfs, ignore_index=True)

    load(full_df)

    logger.info("Pipeline completed successfully for all cities")

if __name__ == "__main__":
    run_pipeline()
