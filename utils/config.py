FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_API_URL = "https://archive-api.open-meteo.com/v1/archive"  # historical

# Cities studied
CITIES = {
    "paris": {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "timezone": "Europe/Paris",
    },
    "hakone_ropeway": {
        "latitude": 35.2452,  # Ropeway summit coordinates - strongest winds
        "longitude": 139.0230,
        "timezone": "Asia/Tokyo",
    },
    "hakone_station": {
        "latitude": 35.2334,  # Hakone city - lower altitude and winds
        "longitude": 139.1038,
        "timezone": "Asia/Tokyo",
    },
    "osaka": {
        "latitude": 34.6937,  # Osaka
        "longitude": 135.5023,
        "timezone": "Asia/Tokyo",
    },
    "kyoto": {
        "latitude": 35.0116,  # Kyoto
        "longitude": 135.7681,
        "timezone": "Asia/Tokyo",
    },
    "kanazawa": {
        "latitude": 36.5613,  # Kanazawa
        "longitude": 136.6562,
        "timezone": "Asia/Tokyo",
    },
    "tokyo": {
        "latitude": 35.6762,  # Tokyo
        "longitude": 139.6503,
        "timezone": "Asia/Tokyo",
    },
    "hiroshima": {
        "latitude": 34.3853,  # Hiroshima - coastal city
        "longitude": 132.4553,
        "timezone": "Asia/Tokyo",
    },
    "miyajima": {
        "latitude": 34.2966,  # Miyajima island - Itsukushima seawater shrine
        "longitude": 132.3198,
        "timezone": "Asia/Tokyo",
    },
}

# Hourly variables to request
HOURLY_VARIABLES = (
    "temperature_2m,"
    "relative_humidity_2m,"
    "precipitation,"
    "wind_speed_10m,"
    "wind_gusts_10m,"
    "cloud_cover," # Visibility proxy
    "snowfall"
)

# Daily variables for sunrise/sunset
DAILY_VARIABLES = "sunrise,sunset"

# File paths
RAW_DATA_DIR = "data/raw"
HOURLY_OUTPUT_CSV_PATH = "data/weather_hourly_multi_city.csv"
MONTHLY_OUTPUT_CSV_PATH = "data/weather_monthly_historical_multi_city.csv"
HISTORICAL_OUTPUT_CSV_PATH = "data/weather_hourly_historical_multi_city.csv"

# Thresholds for analysis
CLEAR_SKY_THRESHOLD = 30.0       # % cloud cover
WIND_SAFE_THRESHOLD_MS = 10.0    # steady wind - for ropeway safety
WIND_GUST_SAFE_THRESHOLD_MS = 30.0 # gusts of wind - for ropeway safety
SNOW_EVENT_THRESHOLD_MM = 5.0    # daily snowfall to count as "snow event"

#BigQuery
BQ_PROJECT_ID = "weather-travel-recommendations"
BQ_DATASET_ID = "weather"
BQ_TABLE_HOURLY_HIST = "hourly_historical"

