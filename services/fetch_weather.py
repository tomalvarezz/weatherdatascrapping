import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser
from functools import lru_cache

from services.constants import (
    CELSIUS_TO_FAHRENHEIT_SCALE,
    CELSIUS_TO_FAHRENHEIT_OFFSET,
    MPS_TO_MPH,
    CITIES
)

load_dotenv()
WEATHER_URL = os.getenv("OPEN_METEO_URL")
GEOCODING_URL = os.getenv("GEOCODING_URL")


def fetch_weather_data():
    return fetch_weather_for_cities([city["City"] for city in CITIES])


# Caches geolocation results to avoid repeating slow external API calls
@lru_cache(maxsize=100)
def get_coordinates(city_name):
    """
    Use the Open-Meteo Geocoding API to get coordinates from a city name.
    This function is cached to avoid redundant external requests.
    """
    response = requests.get(GEOCODING_URL, params={"name": city_name, "count": 1})
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            lat = results[0]["latitude"]
            lon = results[0]["longitude"]
            return lat, lon
    return None, None


def fetch_weather_for_cities(city_list):
    """
    Fetch current weather + humidity from hourly data for each city.
    """
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

            # Match humidity using the closest timestamp to current time
            hourly = data.get("hourly", {})
            if "time" in hourly and "relativehumidity_2m" in hourly:
                current_time_str = current.get("time")
                if current_time_str:
                    # Parse current time and hourly timestamps into datetime objects
                    current_time = parser.parse(current_time_str)
                    hourly_times = [parser.parse(t) for t in hourly["time"]]
                    humidity_values = hourly["relativehumidity_2m"]

                    # Find the closest timestamp index to current time as the humidity is hourly, if not humidity comes as null
                    ## Match current humidity by finding the closest timestamp in the hourly forecast.
                    # This avoids errors due to slight time mismatches (e.g., current time is 14:02 but hourly data is at 14:00).

                    closest_idx = min(
                        range(len(hourly_times)),
                        key=lambda i: abs((hourly_times[i] - current_time).total_seconds())
                    )

                    # Use the closest humidity value
                    humidity = humidity_values[closest_idx]

            # Append processed weather data for the city
            weather_data.append({
                "City": city_name,
                "Temperature (C)": current.get("temperature"),
                "Temperature (F)": round(
                    (current.get("temperature", 0) * CELSIUS_TO_FAHRENHEIT_SCALE) + CELSIUS_TO_FAHRENHEIT_OFFSET, 2
                ),
                "Humidity (%)": humidity,
                "Wind Speed (m/s)": current.get("windspeed"),
                "Wind Speed (mph)": round(current.get("windspeed", 0) * MPS_TO_MPH, 2)
            })

        except Exception as e:
            print(f"Error fetching data for {city_name}: {e}")

    return pd.DataFrame(weather_data)
