import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def transform(raw_data: dict) -> pd.DataFrame:
    """
    Transform raw weather API response into a tabular format.

    grain: 1 row = 1 hourly weather observation for the chosen location
    """

    hourly = raw_data.get("hourly", {})
    if not hourly:
        logger.error("No 'hourly' data found in API response")
        raise ValueError("Missing 'hourly' key in weather data")

    df = pd.DataFrame(hourly)

    # Rename columns for clarity
    df = df.rename(columns={
        "time": "timestamp",
        "temperature_2m": "temperature_c",
        "relative_humidity_2m": "relative_humidity_pct",
    })

    # Optionally ensure correct dtypes
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    logger.info(f"Transformed weather data into DataFrame with {len(df)} rows")
    return df
