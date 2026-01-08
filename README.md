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

This fetches data from the API and loads it into BigQuery:

```
python -m scripts.run_pipeline
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
- Cleans types for downstream daily and monthly metrics

### Planned models (in progress)
- Daily summaries per city (wind, gusts, rain, snow, daytime visibility hours)
- Monthly metrics to compare cities and months:
  - clear-sky ratios
  - rain-free days ratio
  - ropeway “safe days” (daytime wind thresholds)
  - snowfall-related indicators (especially for Kanazawa)
- Travel-oriented “best time to visit” views

## 🎯 Project Purpose
This project is used to:
- Practice Python → BigQuery → dbt on a realistic but manageable dataset
- Explore how raw API data can be turned into clean, queryable models
- Build metrics relevant for trip planning (weather, visibility, ropeway operation)
- Demonstrate an entry-level data engineering / analytics engineering stack
It’s a learning project first, with the bonus of producing data that can genuinely inform future travel decisions.
