import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch
from services import fetch_weather
import pandas as pd

#test get coordinates

@patch("services.fetch_weather.requests.get")
def test_get_coordinates_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{"latitude": 40.7128, "longitude": -74.0060}]
    }
    
    lat, lon = fetch_weather.get_coordinates("New York")
    assert lat == 40.7128
    assert lon == -74.0060

@patch("services.fetch_weather.requests.get")
def test_get_coordinates_not_found(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": []}
    
    lat, lon = fetch_weather.get_coordinates("Unknown")
    assert lat is None
    assert lon is None

# test fetch for cities

@patch("services.fetch_weather.get_coordinates")
@patch("services.fetch_weather.requests.get")
def test_fetch_weather_for_cities(mock_get, mock_coords):
    # Mock coordinates
    mock_coords.return_value = (40.7128, -74.0060)

    # Mock weather API
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "current_weather": {
            "temperature": 20,
            "windspeed": 5,
            "time": "2025-06-22T12:00"
        },
        "hourly": {
            "time": ["2025-06-22T12:00", "2025-06-22T13:00"],
            "relativehumidity_2m": [55, 60]
        }
    }

    df = fetch_weather.fetch_weather_for_cities(["New York"])
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["City"] == "New York"
    assert df.iloc[0]["Temperature (F)"] == 68.0
    assert df.iloc[0]["Humidity (%)"] == 55
    assert df.iloc[0]["Wind Speed (mph)"] == pytest.approx(11.18, 0.01)
