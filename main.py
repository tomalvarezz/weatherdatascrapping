
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse
from services.fetch_weather import fetch_weather_data
from utils.charts import create_bar_chart

#entrypoint for fastAPI

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
      <li><a href="/docs">swagger api docs</a></li>
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
