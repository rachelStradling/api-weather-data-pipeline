from google.cloud import bigquery
from utils.logger import get_logger
from utils.config import BQ_PROJECT_ID, BQ_DATASET_ID, BQ_TABLE_HOURLY_HIST

logger = get_logger(__name__)

def load_to_bigquery(df, table_id: str = None):
    """
    Loads a pandas DataFrame to BigQuery (replaces table).
    """
    client = bigquery.Client(project=BQ_PROJECT_ID)

    table_id = table_id or f"{BQ_PROJECT_ID}.{BQ_DATASET_ID}.{BQ_TABLE_HOURLY_HIST}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # overwrite table
    )

    logger.info(f"Loading {len(df)} rows to BigQuery table: {table_id}")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()

    logger.info("BigQuery load completed")
