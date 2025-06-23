from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse
from typing import List
from schemas.city_request import CityRequest  
from services.fetch_weather import fetch_weather_data, fetch_weather_for_cities
from utils.charts import create_bar_chart

# load default cities dict weather data
df = fetch_weather_data()
df.to_csv("data/weather_data.csv", index=False)

app = FastAPI(title="Weather Data API")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Welcome to the Weather API</h2>
    <ul>
      <li><a href="/csv">Download CSV</a></li>
      <li><a href="/temperature_chart">Temperature Chart</a></li>
      <li><a href="/humidity_chart">Humidity Chart</a></li>
      <li><a href="/docs">Swagger API docs</a></li>
    </ul>
    """

@app.get("/csv")
def get_csv():
    return FileResponse("data/weather_data.csv", filename="weather_data.csv")

@app.get("/temperature_chart")
def get_temperature_chart():
    buffer = create_bar_chart(df, "Temperature (C)", "Temperature by City", "°C")
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/humidity_chart")
def get_humidity_chart():
    buffer = create_bar_chart(df, "Humidity (%)", "Humidity by City", "%")
    return StreamingResponse(buffer, media_type="image/png")


# dynamic city list via HTTP post, that uses geo location for lat long custom via city name

@app.post("/custom_weather")
def custom_weather(req: CityRequest):
    df_custom = fetch_weather_for_cities(req.cities)
    df_custom.to_csv("data/custom_weather_data.csv", index=False)
    return df_custom.to_dict(orient="records")
