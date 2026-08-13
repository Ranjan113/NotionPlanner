from langchain.tools import tool
import requests


@tool
def get_weather(city:str) -> str:
    """Get the weather for a given city"""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_data = requests.get(geo_url).json()

        if not geo_data.get('results'):
            return {"error":f"City '{city}' not found"}

        location = geo_data['results'][0]
        lat, lon = location['latitude'], location['longitude']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
        data = requests.get(weather_url).json()
        
        temp = data['current']['temperature_2m']
        return {'city':city,'temp':temp,'unit':'C'}

    except Exception as e:
        return {'error':str(e)}
        