import requests 
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather(city: str) -> str:
    "takes a city name and returns current weather information"

    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data["cod"]!=200:
            return f'city not found: {city}'
        
        weather_info = (
            f"City: {data['name']}, {data['sys']['country']}\n"
            f"Temperature: {data['main']['temp']}°C\n"
            f"Feels Like: {data['main']['feels_like']}°C\n"
            f"Condition: {data['weather'][0]['description']}\n"
            f"Humidity: {data['main']['humidity']}%\n"
            f"Wind Speed: {data['wind']['speed']} m/s\n"
        )

        return weather_info
    
    except Exception as e:
        return f'Weather fetch failed: {str(e)}'
