import os
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse

# load api bonus 
load_dotenv()
API_BASE = os.getenv("OPEN_METEO_URL")

# unit conversion constants for readability
CELSIUS_TO_FAHRENHEIT_SCALE = 9 / 5
CELSIUS_TO_FAHRENHEIT_OFFSET = 32
MPS_TO_MPH = 2.23694


# cities dict
cities = [
    {"City": "New York", "Latitude": 40.7128, "Longitude": -74.0060},
    {"City": "Tokyo", "Latitude": 35.6895, "Longitude": 139.6917},
    {"City": "London", "Latitude": 51.5074, "Longitude": -0.1278},
    {"City": "Paris", "Latitude": 48.8566, "Longitude": 2.3522},
    {"City": "Berlin", "Latitude": 52.5200, "Longitude": 13.4050},
    {"City": "Sydney", "Latitude": -33.8688, "Longitude": 151.2093},
    {"City": "Mumbai", "Latitude": 19.0760, "Longitude": 72.8777},
    {"City": "Cape Town", "Latitude": -33.9249, "Longitude": 18.4241},
    {"City": "Moscow", "Latitude": 55.7558, "Longitude": 37.6173},
    {"City": "Rio de Janeiro", "Latitude": -22.9068, "Longitude": -43.1729}
]

# for future buildup of the dataframe
weather_data = []

for city in cities:
    city_name = city["City"]
    lat = city["Latitude"]
    lon = city["Longitude"]

    # NOTE api does not return on current weather condition, the humidity, so it should be fetched with parameter  "hourly": "relativehumidity_2m"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "relativehumidity_2m",
        "timezone": "auto"
    }

    try:
        response = requests.get(API_BASE, params=params)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather", {})
        humidity = None

        if "time" in data.get("hourly", {}) and "relativehumidity_2m" in data["hourly"]:
            time_list = data["hourly"]["time"]
            humidity_list = data["hourly"]["relativehumidity_2m"]
            current_time = current.get("time")
            if current_time in time_list:
                idx = time_list.index(current_time)
                humidity = humidity_list[idx]

        weather_data.append({
    "City": city_name,
    "Temperature (C)": current.get("temperature"),
    "Temperature (F)": round(
        (current.get("temperature", 0) * CELSIUS_TO_FAHRENHEIT_SCALE) + CELSIUS_TO_FAHRENHEIT_OFFSET, 2
    ),
    "Humidity (%)": humidity,
    "Wind Speed (m/s)": current.get("windspeed"),
    "Wind Speed (mph)": round(
        current.get("windspeed", 0) * MPS_TO_MPH, 2
    )
})

    except Exception as e:
        print(f"Error fetching data for {city_name}: {e}")

# create dataframe and save to response csv
df = pd.DataFrame(weather_data)
df.to_csv("weather_data.csv", index=False)

# fast api up
app = FastAPI(title="Weather Data API")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Welcome to the Weather API</h2>
    <p>Available endpoints:</p>
    <ul>
      <li><a href="/csv">Download CSV</a></li>
      <li><a href="/temperature_chart">View Temperature Chart</a></li>
      <li><a href="/humidity_chart">View Humidity Chart</a></li>
      <li><a href="/docs">Swagger API Docs</a></li>
    </ul>
    """

@app.get("/csv")
def get_csv():
    return FileResponse("weather_data.csv", filename="weather_data.csv")

@app.get("/temperature_chart")
def temperature_chart():
    fig, ax = plt.subplots()
    df_sorted = df.sort_values("Temperature (C)", ascending=False)
    ax.bar(df_sorted["City"], df_sorted["Temperature (C)"])
    ax.set_title("Temperature by City")
    ax.set_ylabel("°C")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/humidity_chart")
def humidity_chart():
    fig, ax = plt.subplots()
    df_sorted = df.sort_values("Humidity (%)", ascending=False)
    ax.bar(df_sorted["City"], df_sorted["Humidity (%)"])
    ax.set_title("Humidity by City")
    ax.set_ylabel("%")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
