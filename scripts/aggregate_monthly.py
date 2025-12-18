import pandas as pd
from utils.logger import get_logger
from utils.config import (
    HISTORICAL_OUTPUT_CSV_PATH,
    MONTHLY_OUTPUT_CSV_PATH,
    CLEAR_SKY_THRESHOLD,
    WIND_SAFE_THRESHOLD_MS,
    SNOW_EVENT_THRESHOLD_MM,
)

logger = get_logger(__name__)

def aggregate_monthly():
    df = pd.read_csv(HISTORICAL_OUTPUT_CSV_PATH)
    if df.empty:
        raise ValueError("Hourly data is empty")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    df["year_month"] = df["timestamp"].dt.to_period("M").astype(str)

    # Helper columns
    df["is_daytime_clear"] = df["is_daytime"] & (df["cloud_cover"] < CLEAR_SKY_THRESHOLD)
    df["has_snow"] = df["snowfall"] > 0

    # ---- DAILY AGGREGATION ----
    daily = df.groupby(["city", "year_month", "date"]).agg(
        avg_temp_c=("temperature_c", "mean"),
        max_wind_speed=("wind_speed_10m", "max"),
        max_wind_gust=("wind_gusts_10m", "max"),
        total_precip=("precipitation", "sum"),
        total_snowfall=("snowfall", "sum"),
        snow_hours=("has_snow", "sum"),
        daytime_hours=("is_daytime", "sum"),
        daytime_clear_hours=("is_daytime_clear", "sum"),
    ).reset_index()

    # Flags per day
    daily["is_ropeway_safe_day"] = (
    (daily["max_wind_speed"] < WIND_SAFE_THRESHOLD_MS)
    & (daily["max_wind_gust"] < WIND_GUST_SAFE_THRESHOLD_MS)
        )
    daily["is_rain_free_day"] = daily["total_precip"] == 0
    daily["is_snow_event_day"] = daily["total_snowfall"] > SNOW_EVENT_THRESHOLD_MM

    # ---- MONTHLY AGGREGATION ----
    monthly = daily.groupby(["city", "year_month"]).agg(
        avg_temp_c=("avg_temp_c", "mean"),
        max_wind_speed_month=("max_wind_speed", "max"),
        total_precipitation=("total_precip", "sum"),
        total_snowfall=("total_snowfall", "sum"),
        total_snow_hours=("snow_hours", "sum"),
        total_daytime_hours=("daytime_hours", "sum"),
        total_daytime_clear_hours=("daytime_clear_hours", "sum"),
        ropeway_safe_days=("is_ropeway_safe_day", "sum"),
        rain_free_days=("is_rain_free_day", "sum"),
        snow_event_days=("is_snow_event_day", "sum"),
        n_days=("date", "nunique"),
    ).reset_index()

    # Final ratios
    monthly["daytime_clear_sky_hours_ratio"] = (
        monthly["total_daytime_clear_hours"] / monthly["total_daytime_hours"]
    ).fillna(0)

    monthly["ropeway_safe_days_ratio"] = (
        monthly["ropeway_safe_days"] / monthly["n_days"]
    ).fillna(0)

    monthly["rain_free_days_ratio"] = (
        monthly["rain_free_days"] / monthly["n_days"]
    ).fillna(0)

    # Avoid division by zero for snow intensity
    monthly["avg_snow_intensity"] = 0.0
    mask_snow = monthly["total_snow_hours"] > 0
    monthly.loc[mask_snow, "avg_snow_intensity"] = (
        monthly.loc[mask_snow, "total_snowfall"] / monthly.loc[mask_snow, "total_snow_hours"]
    )

    # You can drop intermediate columns if you want cleaner output
    monthly.to_csv(MONTHLY_OUTPUT_CSV_PATH, index=False)
    logger.info(f"Saved monthly metrics to {MONTHLY_OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    aggregate_monthly()
