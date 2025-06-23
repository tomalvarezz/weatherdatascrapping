# services/fetch_weather.py

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from services.constants import CELSIUS_TO_FAHRENHEIT_SCALE, CELSIUS_TO_FAHRENHEIT_OFFSET, MPS_TO_MPH,CITIES

load_dotenv()
WEATHER_URL = os.getenv("OPEN_METEO_URL")
GEOCODING_URL = os.getenv("GEOCODING_URL")

def fetch_weather_data():
    return fetch_weather_for_cities([city["City"] for city in CITIES])


def get_coordinates(city_name):
    response = requests.get(GEOCODING_URL, params={"name": city_name, "count": 1})
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            lat = results[0]["latitude"]
            lon = results[0]["longitude"]
            return lat, lon
    return None, None

def fetch_weather_for_cities(city_list):
    weather_data = []

    for city_name in city_list:
        lat, lon = get_coordinates(city_name)
        if lat is None:
            print(f"Skipping city '{city_name}': coordinates not found")
            continue

        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "relativehumidity_2m",
            "timezone": "auto"
        }

        try:
            response = requests.get(WEATHER_URL, params=params)
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
                "Temperature (F)": round((current.get("temperature", 0) * CELSIUS_TO_FAHRENHEIT_SCALE) + CELSIUS_TO_FAHRENHEIT_OFFSET, 2),
                "Humidity (%)": humidity,
                "Wind Speed (m/s)": current.get("windspeed"),
                "Wind Speed (mph)": round(current.get("windspeed", 0) * MPS_TO_MPH, 2)
            })

        except Exception as e:
            print(f"Error fetching data for {city_name}: {e}")

    return pd.DataFrame(weather_data)
