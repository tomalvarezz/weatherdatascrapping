# Weather Data Scraper + Dashboards and Swagger Docs  

by Tomas Alvarez Escalante

This project fetches real-time weather data from the [Open-Meteo](https://open-meteo.com/en/docs) public API, processes it, generates a CSV file, and exposes visualizations through a FastAPI-based web server.

---

## How to Run

1. Create a `.env` file in the project root with the following content:

    ```
    OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast
    GEOCODING_URL=https://geocoding-api.open-meteo.com/v1/search
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the FastAPI server using Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

4. Access the app in your browser:

- `http://127.0.0.1:8000/` – Welcome page  
- `http://127.0.0.1:8000/docs` – Swagger UI (API documentation)  
- `http://127.0.0.1:8000/csv` – Download the CSV file  
- `http://127.0.0.1:8000/temperature_chart` – Temperature chart (PNG)  
- `http://127.0.0.1:8000/humidity_chart` – Humidity chart (PNG)

---

## Features

- Retrieves current weather data (temperature, humidity, wind speed) for 10 global cities.
- Converts units:
  - Temperature: Celsius → Fahrenheit
  - Wind Speed: m/s → mph
- Filters and rankings:
  - Top cities by highest temperature
  - Top cities by lowest humidity
- Exports processed data to a `CSV` file.
- Provides visualizations:
  - Temperature by city
  - Humidity by city
- FastAPI web server with endpoints:
  - `/csv`: download the CSV file
  - `/temperature_chart`: temperature bar chart
  - `/humidity_chart`: humidity bar chart
- Custom city support:
  - Accepts a list of cities via HTTP POST and generates a `custom_weather_data.csv`.
  - You can test this using a `.http` file with the REST Client extension in VSCode or any client of your choice.

---

## Project Structure

weather_app/
├── main.py # FastAPI entrypoint, handles routing and API exposure (controller)
├── services/
│ ├── fetch_weather.py # Handles Open-Meteo API calls and weather data processing
│ └── constants.py # Constants for unit conversions and predefined city list
├── utils/
│ └── charts.py # Chart generation using matplotlib
├── data/
│ └── weather_data.csv # Auto-generated CSV with processed weather data
├── schemas/
│ └── city_request.py # Request model schema for POST input
├── tests/
│ └── test_fetch_weather.py # Unit tests using pytest and mock
├── .env # Environment variables for API URLs
├── requirements.txt # Python dependencies
└── README.md # Documentation (this file)

## Dependencies

```bash
fastapi
uvicorn
python-dotenv
python-dateutil
pandas
requests
matplotlib
