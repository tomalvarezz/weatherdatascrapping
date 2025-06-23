# Weather Data Scraper + Dashboards and Swagger Docs by Tomas Alvarez Escalante

This project fetches real-time weather data from the [Open-Meteo](https://open-meteo.com/en/docs) public API, processes the data, generates a CSV file, and exposes visualizations through a FastAPI-based web server.

---

## How to run?

- Create a .env file in the project root with the following content:
    OPEN_METEO_URL=<https://api.open-meteo.com/v1/forecast>

- Start the FastAPI server using Uvicorn:
    uvicorn main:app --reload

-Open the browser, and access the app at

    <http://127.0.0.1:8000/> – Welcome page

    <http://127.0.0.1:8000/docs> – Swagger UI (API documentation)

    <http://127.0.0.1:8000/csv> – Download the CSV file

    <http://127.0.0.1:8000/temperature_chart> – Temperature chart (PNG)

    <http://127.0.0.1:8000/humidity_chart> – Humidity chart (PNG)

## Features

- Retrieves current weather data (temperature, humidity, wind speed) for 10 global cities.
- Converts units:
  - Temperature: Celsius → Fahrenheit
  - Wind Speed: m/s → mph
- Exports processed data to a `CSV` file.
- Provides visualizations:
  - Temperature by city
  - Humidity by city
- FastAPI web server with endpoints:
  - `/csv`: download the CSV file
  - `/temperature_chart`: temperature bar chart
  - `/humidity_chart`: humidity bar chart

---

## Project structure

weather_app/
├── main.py                  # FastAPI entrypoint, handles routing and API exposure  (controller)
├── services/
│   ├── fetch_weather.py     # handles the the Open-Meteo API calls and processing weather data
│   └── constants.py         # constant utils for unit conversions and the list of predefined cities
├── utils/
│   └── charts.py            # chart generation functions using matplotlib
├── data/
│   └── weather_data.csv     # auto-generated csv containing the processed weather data
├── schemas/
│   └── city_request.py      # request model for http method
├── .env                     # base url from the API
├── requirements.txt         # dependencies for python
└── README.md                # documentation

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
