# Weather Data Project – Travel Planning
This project collects weather data for several cities (mainly in Japan) and uses it to answer practical travel questions, such as:
- When is the best time of year to visit a city?
- Which months have clearer skies or less rain?
- How often is the Hakone ropeway likely to be open?
- If I’m visiting soon, which days are better for visibility?

The goal is to practice building a small but realistic data pipeline and to explore how weather data can be used for decision-making.

# What this project does
The project has two main parts:
## 1. Historical data (planning ahead)
Uses historical weather data (archive API)
Collects hourly data for each city
Aggregates it into monthly metrics, such as:
- share of clear daytime hours
- number of rain-free days
- number of snow days
- days safe for the Hakone ropeway (low wind)

This is used to understand seasonal patterns and decide when to travel.
## 2. Forecast data (on site)
Uses short-term weather forecasts
Intended for day-by-day decisions once the trip is close
Not aggregated monthly (forecast is too short for that)

# Data source
Weather data comes from Open-Meteo:
- Forecast API for short-term weather
- Archive API for historical weather
- No API key is required.

# How to run the project
## 1. Fetch historical data (example: all of 2025)
`python -m scripts.fetch_historical --start-date 2025-01-01 --end-date 2025-12-31`
This creates an hourly historical dataset for all configured cities.
## 2. Create monthly metrics from historical data
`python -m scripts.aggregate_monthly`
This produces a monthly dataset with travel-oriented metrics.
## 3. (Optional) Fetch forecast data
`python -m scripts.run_pipeline`
This fetches short-term forecast data, useful for on-site planning.


# Notes
- Cities, weather variables, and thresholds are defined in utils/config.py
- The project focuses on clarity and learning, not performance or scale
- This is a learning project, not a production system
