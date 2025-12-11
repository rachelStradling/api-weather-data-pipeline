from utils.logger import get_logger
from utils.config import OUTPUT_CSV_PATH

logger = get_logger(__name__)

def load(df):
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    logger.info(f"Loaded {len(df)} rows into {OUTPUT_CSV_PATH}")
