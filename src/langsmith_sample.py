import json
import urllib.error
import urllib.parse
import urllib.request

from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

_WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


def get_weather(city: str) -> str:
    """Get the current weather for a city from Open-Meteo."""
    try:
        place = _geocode(city)
        if place is None:
            return f"No location found for {city}."

        current, units = _current_weather(place["latitude"], place["longitude"])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
        return f"Weather lookup failed for {city}: {exc}"

    condition = _WEATHER_CODES.get(current["weather_code"], "unknown conditions")
    label = ", ".join(
        part
        for part in (place.get("name"), place.get("admin1"), place.get("country"))
        if part
    )
    return (
        f"{label}: {condition}, "
        f"{current['temperature_2m']}{units['temperature_2m']}, "
        f"humidity {current['relative_humidity_2m']}{units['relative_humidity_2m']}, "
        f"wind {current['wind_speed_10m']} {units['wind_speed_10m']}."
    )


def _geocode(city: str) -> dict | None:
    query = urllib.parse.urlencode(
        {"name": city, "count": 1, "language": "en", "format": "json"}
    )
    payload = _get_json(f"https://geocoding-api.open-meteo.com/v1/search?{query}")
    results = payload.get("results") or []
    return results[0] if results else None


def _current_weather(latitude: float, longitude: float) -> tuple[dict, dict]:
    query = urllib.parse.urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto",
        }
    )
    payload = _get_json(f"https://api.open-meteo.com/v1/forecast?{query}")
    return payload["current"], payload["current_units"]


def _get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "langchain-graph-rag"})
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


agent = create_agent(
    model="openai:gpt-6-luna",
    tools=[get_weather],
    system_prompt="""You are a professional weather forecaster. 
    You are given a city and you need to forecast the weather for that city.""",
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in manchester?"}]}
)

response_text = response['messages'][-1].content[0]['text']
print(f"\n{response_text}\n")
