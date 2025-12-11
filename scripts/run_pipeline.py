from pipelines.extract import extract
from pipelines.transform import transform
from pipelines.load import load
from utils.logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    logger.info("Starting pipeline")
    raw = extract()
    df = transform(raw)
    load(df)
    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()
