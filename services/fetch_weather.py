#API call handler
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from services.constants import CITIES, CELSIUS_TO_FAHRENHEIT_SCALE, CELSIUS_TO_FAHRENHEIT_OFFSET, MPS_TO_MPH

load_dotenv()
API_BASE = os.getenv("OPEN_METEO_URL")

def fetch_weather_data():
    weather_data = []

    for city in CITIES:
        city_name = city["City"]
        lat = city["Latitude"]
        lon = city["Longitude"]

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

            hourly = data.get("hourly", {})
            if "time" in hourly and "relativehumidity_2m" in hourly:
                current_time = current.get("time")
                if current_time in hourly["time"]:
                    idx = hourly["time"].index(current_time)
                    humidity = hourly["relativehumidity_2m"][idx]

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

    return pd.DataFrame(weather_data)
