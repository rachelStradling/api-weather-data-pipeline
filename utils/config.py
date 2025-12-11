WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Coordinates for Paris
LATITUDE = 48.8566
LONGITUDE = 2.3522

# Parameters for the API call
WEATHER_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "temperature_2m,relative_humidity_2m,precipitation",
    "timezone": "Europe/Paris",
}

# File paths
RAW_DATA_PATH = "data/raw/weather.json"
OUTPUT_CSV_PATH = "data/weather_hourly.csv"
