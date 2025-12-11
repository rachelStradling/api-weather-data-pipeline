This project demonstrates a simple but robust end-to-end data pipeline built in Python.
It extracts hourly weather data from the Open-Meteo API, transforms it into a clean tabular format, and stores it locally as a CSV ready for analysis.
The goal is to show how to structure data workflows like a pipeline, not a one-off script — following analytics engineering best practices.


🔧 Tech Stack
Python 3.14
Requests → API ingestion
Pandas → transformation
Pytest → small test for transformation logic
Simple logging for observability
Local CSV output (can easily be extended to BigQuery)

🌦️ Data Source: Open-Meteo Weather API
API: https://open-meteo.com
No API key required
Location used (default): Paris, France
Grain of final dataset:
➝ 1 row = 1 hourly weather observation

▶️ How to Run the Pipeline
1. Activate virtual environment
Run the command "source .venv/bin/activate"
2. Install dependencies
Run the command "pip install -r requirements.txt"
3. Run the pipeline
Run the command "python -m scripts.run_pipeline"
4. Check your outputs
data/raw/weather.json
data/weather_hourly.csv
