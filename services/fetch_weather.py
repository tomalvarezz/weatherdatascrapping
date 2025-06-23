# services/fetch_weather.py

import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser

# Import constants for unit conversion and default cities
from services.constants import (
    CELSIUS_TO_FAHRENHEIT_SCALE,
    CELSIUS_TO_FAHRENHEIT_OFFSET,
    MPS_TO_MPH,
    CITIES
)

# Load environment variables from .env file
load_dotenv()
WEATHER_URL = os.getenv("OPEN_METEO_URL")
GEOCODING_URL = os.getenv("GEOCODING_URL")

# Fetch weather for the predefined list of cities
def fetch_weather_data():
    return fetch_weather_for_cities([city["City"] for city in CITIES])

# Use Open-Meteo Geocoding API to get coordinates (lat/lon) from city name
def get_coordinates(city_name):
    response = requests.get(GEOCODING_URL, params={"name": city_name, "count": 1})
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            lat = results[0]["latitude"]
            lon = results[0]["longitude"]
            return lat, lon
    return None, None

# Core logic: fetch current weather + nearest humidity for a list of city names (nearest meaning hourly relative humidity)
def fetch_weather_for_cities(city_list):
    weather_data = []
#Unluckily this is one city per request, it would be better to pass a city list as we would have less external api calls, luckily they are free but might generate overhead
    for city_name in city_list:
        lat, lon = get_coordinates(city_name)
        if lat is None:
            print(f"Skipping city '{city_name}': coordinates not found")
            continue  # skip cities we can't geolocate

        # Parameters for the Open-Meteo weather API
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "hourly": "relativehumidity_2m",  # get hourly humidity as current weather condition needs it
            "timezone": "auto"  # auto-align timezones to local city time
        }

        try:
            response = requests.get(WEATHER_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract current weather block (temp, wind, timestamp)
            current = data.get("current_weather", {})
            humidity = None  # initialize

            # Match humidity using the closest timestamp to current time as it was previously failing due to hour vs timestamp mismatch
            hourly = data.get("hourly", {})
            if "time" in hourly and "relativehumidity_2m" in hourly:
                current_time_str = current.get("time")

                 # Converts all hourly timestamps into datetime objects.
                 #Extracts the corresponding list of humidity values (1 per hour).
                
                if current_time_str:
                    current_time = parser.parse(current_time_str)
                    hourly_times = [parser.parse(t) for t in hourly["time"]]
                    humidity_values = hourly["relativehumidity_2m"]

                    # Match the closest humidity value by comparing timestamps
                    #For each index i, compute the time difference between hourly_times[i] and current_time.
                    #Find the index closest_idx with the smallest time difference → i.e., the closest humidity reading.
                    
                    closest_idx = min(
                        range(len(hourly_times)),
                        key=lambda i: abs((hourly_times[i] - current_time).total_seconds())
                    )
                    humidity = humidity_values[closest_idx]

            # Append processed data to list
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

    # Return final DataFrame with all city data
    return pd.DataFrame(weather_data)
