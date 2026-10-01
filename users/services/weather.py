import requests
from datetime import datetime, timedelta

_cached_weather = None
_cached_at = None

def get_weekend_forecast(lat, lon):
    global _cached_weather, _cached_at

    # Cache for 30 minutes
    if _cached_at and datetime.now() - _cached_at < timedelta(minutes=30):
        return _cached_weather

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,rain,showers,wind_speed_10m,wind_speed_80m,weather_code,temperature_80m,precipitation"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=Europe/Dublin"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})
        dates = daily.get("time", [])
        codes = daily.get("weather_code", [])
        tmax = daily.get("temperature_2m_max", [])
        tmin = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])

        today = datetime.now().date()
        saturday = today + timedelta(days=(5 - today.weekday()) % 7)
        sunday = saturday + timedelta(days=1)

        weekend = {}

        for i, d in enumerate(dates):
            date_obj = datetime.strptime(d, "%Y-%m-%d").date()

            if date_obj == saturday:
                weekend["saturday"] = {
                    "date": date_obj,
                    "code": codes[i],
                    "tmax": tmax[i],
                    "tmin": tmin[i],
                    "precip": precip[i],
                }

            if date_obj == sunday:
                weekend["sunday"] = {
                    "date": date_obj,
                    "code": codes[i],
                    "tmax": tmax[i],
                    "tmin": tmin[i],
                    "precip": precip[i],
                }

        # Save cache
        _cached_weather = weekend
        _cached_at = datetime.now()

        return weekend

    except Exception as e:
        print("Weather fetch error:", e)
        return _cached_weather  # fallback to last known good value





WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate showers",
    82: "Violent showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Severe hailstorm",
}

def describe(code):
    return WEATHER_DESCRIPTIONS.get(code, "Unknown")
