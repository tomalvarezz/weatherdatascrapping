# weather data scrapper + dashboards and swagger docs

this project fetches real-time weather data from the [Open-Meteo](https://open-meteo.com/en/docs) public API, processes the data, generates a CSV file, and exposes visualizations through a FastAPI-based web server.

---

## features that can be used

- retrieves current weather data (temperature, humidity, wind speed) for 10 global cities.
- converts units:
  - temperature: Celsius → Fahrenheit
  - wind speed: m/s → mph
- exports processed data to a `CSV` file.
- provides visualizations:
  - temperature by city
  - humidity by city
- FastAPI web server with endpoints:
  - `/csv`: download the CSV file
  - `/temperature_chart`: temperature bar chart
  - `/humidity_chart`: humidity bar chart

---

## requirements

install dependencies with:
pip install -r requirements.txt

Tomas Alvarez Escalante
