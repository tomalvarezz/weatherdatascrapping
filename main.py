from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse, JSONResponse
from typing import List
from schemas.city_request import CityRequest  
from services.fetch_weather import fetch_weather_data, fetch_weather_for_cities
from utils.charts import create_bar_chart

## Below is basically the app controller , entrypoint for FastAPI

# load default cities dict weather data
df = fetch_weather_data()
df.to_csv("data/weather_data.csv", index=False)

app = FastAPI(title="Weather Data API")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Weather API</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f4f4f4; color: #333; }
            h1 { color: #2c3e50; }
            ul { line-height: 1.8; }
            a { color: #2980b9; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>🌤️ Weather Data Dashboard</h1>
        <p>Welcome to the weather data API. You can:</p>
        <ul>
            <li><a href="/docs">Explore the API (Swagger Docs)</a></li>
            <li><a href="/csv">Download Weather CSV</a></li>
            <li><a href="/temperature_chart">View Temperature Chart (°C)</a></li>
            <li><a href="/temperature_f_chart">View Temperature Chart (°F)</a></li>
            <li><a href="/humidity_chart">View Humidity Chart</a></li>
            <li><a href="/wind_chart">View Wind Speed Chart (m/s)</a></li>
            <li><a href="/wind_mph_chart">View Wind Speed Chart (mph)</a></li>
        </ul>
    </body>
    </html>
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

@app.get("/wind_chart")
def get_wind_chart():
    buffer = create_bar_chart(df, "Wind Speed (m/s)", "Wind Speed by City", "m/s")
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/wind_mph_chart")
def get_wind_mph_chart():
    buffer = create_bar_chart(df, "Wind Speed (mph)", "Wind Speed (mph) by City", "mph")
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/temperature_f_chart")
def get_temperature_f_chart():
    buffer = create_bar_chart(df, "Temperature (F)", "Temperature (F) by City", "°F")
    return StreamingResponse(buffer, media_type="image/png")


# dynamic city list via HTTP post, that uses geo location for lat long custom via city name

@app.post("/custom_weather")
def custom_weather(req: CityRequest):
    df_custom = fetch_weather_for_cities(req.cities)
    df_custom.to_csv("data/custom_weather_data.csv", index=False)
    return df_custom.to_dict(orient="records")

##Rankings and filters using pandas directly

@app.get("/top_temperature")
def get_top_temperature(n: int = 5):
    top_temp = df.sort_values(by="Temperature (C)", ascending=False).head(n)
    return JSONResponse(content=top_temp.to_dict(orient="records"))

@app.get("/lowest_humidity")
def get_lowest_humidity(n: int = 5):
    low_humidity = df.sort_values(by="Humidity (%)", ascending=True).head(n)
    return JSONResponse(content=low_humidity.to_dict(orient="records"))

@app.get("/top_wind_speed")
def get_top_wind_speed(n: int = 5):
    top_wind = df.sort_values(by="Wind Speed (mph)", ascending=False).head(n)
    return JSONResponse(content=top_wind.to_dict(orient="records"))
