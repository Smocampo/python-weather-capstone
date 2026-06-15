# python-weather-capstone
# Sofia Ocampo-Morales

# 2026 World Cup Host Cities Weather Tracker

An end-to-end data pipeline and web application built for the Code The Dream Python Capstone.

## Features
- **Web Scraping (`src/scraper.py`):** Uses Selenium WebDriver to securely extract real-time weather metrics for all 16 FIFA World Cup 2026 host cities.
- **Data Pipeline (`src/pipeline.py`):** Leverages Pandas to clean data types, filter duplicates, and migrate records into a relational database.
- **Database Storage:** Saves data locally into a structured SQLite database (`data/weather_data.db`).
- **Web Dashboard (`app.py`):** Displays data dynamically using an interactive Streamlit UI complete with metrics and comparative charting.

## How to Run
1. Run `pip install -r requirements.txt`
2. Run the scraper: `python src/scraper.py` (or `python3`)
3. Run the pipeline: `python src/pipeline.py`
4. Launch the dashboard: `streamlit run app.py`

