# Weather Travel Data Pipeline

A small end-to-end project to practice a modern data engineering / analytics stack using real weather data.

The pipeline collects hourly weather conditions from the Open-Meteo API, stores them in BigQuery, and transforms them with dbt to produce clean models and travel-relevant metrics (clear-sky ratios, ropeway safety days, rainfall patterns, etc.).  
The long-term goal is to make it easier to evaluate the best time of year to visit Japanese destinations like Hakone, Kanazawa, Osaka, and more.

---

## 🧭 Project Overview

**Flow:**

1. **Python**
   - Fetches raw weather data (hourly + historical) from the Open-Meteo API  
   - Prepares the data for loading  
   - Loads it into the BigQuery dataset `weather`

2. **BigQuery**
   - Stores all raw weather data (hourly historical for multiple cities)
   - Acts as the central warehouse for transformations and analysis

3. **dbt**
   - Builds cleaned/staging models on top of the raw tables
   - Adds typed columns (proper datetimes, day/night flags)
   - Will gradually add daily and monthly metrics

This structure is intentionally simple but mirrors a real analytics engineering setup.

---

## ⚙️ Local Setup

### 1. Python environment

From the project root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Run the ingestion Pipeline

This downloads raw archive data from the API and transforms it into an hourly table:

```
python -m scripts.fetch_historical
```

Then to load the data to bigquery

```
python -m scripts.load_historical_to_bigquery
```

## 📦 dbt Setup

dbt uses a separate local configuration file for connection details:
```
~/.dbt/profiles.yml
```

Example profile (BigQuery + OAuth):
```
weather_dbt:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: weather-travel-recommendations
      dataset: weather_dbt_dev
      location: EU
      threads: 2
```

Run dbt commands from the dbt project folder:
```
cd dbt/weather_dbt
dbt debug    # check connection to BigQuery
dbt run      # build models
```

## 📊 Current dbt Models

### stg_hourly_historical


Staging model that:
- Reads raw weather data from ```weather.hourly_historical``` in BigQuery
- Casts sunrise and sunset from strings to proper DATETIME fields
- Derives a ```hour_dt``` helper column from the ```timestamp```
- Recomputes ```is_daytime``` based on sunrise/sunset boundaries
- Cleans types for downstream logic

### int_weather_daily
Intermediate model that aggregates hourly weather into daily summaries per city.
Used as the foundation for monthly and travel-oriented metrics.
It includes:
- avg_temp_c → average temperature of the day
- max_daytime_wind_speed / max_daytime_wind_gust → daytime-only wind measures
- rain_free_day → TRUE if no precipitation
- snow_event_day → TRUE if any snowfall
- daytime_hours / daytime_clear_hours → visibility proxies
- ropeway_safe_day → TRUE if daytime wind & gusts stay under Hakone ropeway safety thresholds
This is the main transformation layer where definitions (e.g., wind thresholds) can be adjusted.

### mart_weather_monthly
Monthly “travel metrics” aggregated from ```int_weather_daily```.
This model is designed to answer questions like “Which month is best to visit Hakone?” or “Which cities have the clearest skies in winter?”.
It provides:
- avg_monthly_temp_c
- rain_free_days_ratio
- snow_event_days_ratio
- avg_snow_intensity_mm
- daytime_clear_sky_hours_ratio
- ropeway_safe_days_ratio → % of days where ropeway-safe winds occur
- days_in_month_with_data
This model could be used in BI tools or in analysis.

## 📘 Model Documentation (YAML)
dbt uses YAML files to document models and columns and to attach basic tests.
This project contains a models/schema.yml file describing:
- what each model represents
- what each column means
- data-quality tests (not_null, ...)

Hence, running the following code will generate project documentation:
```
dbt docs generate
dbt docs serve
```

## 🎯 Project Purpose
This project is used to:
- practice a realistic DE/AE stack
combine Python ingestion with BigQuery storage
- explore dbt for modeling, documentation, and testing
- build clean weather datasets for trip planning
- compute metrics relevant to Japanese travel (visibility, wind, ropeway safety, rainfall, snow)
It’s both a learning project and a practical dataset for planning future trips.
