import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def transform(raw_data: dict, city_name: str) -> pd.DataFrame:
    hourly = raw_data.get("hourly", {})
    if not hourly:
        logger.error(f"No 'hourly' data found for {city_name}")
        raise ValueError("Missing 'hourly' key in weather data")

    df = pd.DataFrame(hourly)
    df = df.rename(columns={
        "time": "timestamp",
        "temperature_2m": "temperature_c",
        "relative_humidity_2m": "relative_humidity_pct",
    })
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["city"] = city_name

    # Daytime flag using sunrise/sunset
    daily = raw_data.get("daily", {})
    if daily:
        df_daily = pd.DataFrame(daily)
        df_daily["date"] = pd.to_datetime(df_daily["time"]).dt.date
        df_daily["sunrise"] = pd.to_datetime(df_daily["sunrise"])
        df_daily["sunset"] = pd.to_datetime(df_daily["sunset"])

        # Add date to hourly df
        df["date"] = df["timestamp"].dt.date

        # Merge sunrise/sunset onto each hourly row
        df = df.merge(
            df_daily[["date", "sunrise", "sunset"]],
            on="date",
            how="left"
        )

        df["is_daytime"] = (df["timestamp"] >= df["sunrise"]) & (df["timestamp"] <= df["sunset"])
    else:
        logger.warning(f"No 'daily' data for {city_name}, cannot compute is_daytime")
        df["is_daytime"] = False

    return df
