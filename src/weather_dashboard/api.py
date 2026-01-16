"""
Module for handling OpenWeatherMap API connections and data retrieval.
"""
import requests
import os
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode


class WeatherAPI:
    """
    Class to handle interactions with the OpenWeatherMap API
    """

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the WeatherAPI class

        Args:
            api_key: OpenWeatherMap API key. If not provided, will try to load from environment
        """
        self.api_key = api_key or self._load_api_key()

        if not self.api_key:
            raise ValueError(
                "No API key provided. Please set OPENWEATHER_API_KEY environment variable "
                "or pass the key as an argument."
            )
    def _load_api_key(self) -> Optional[str]:

        """
        Load API key from environment variable
        """
        api_key = os.getenv('OPENWEATHER_API_KEY')

        # Try to load from .env file if python-dotenv is available
        if not api_key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.getenv('OPENWEATHER_API_KEY')
            except ImportError:
                pass  # dotenv not installed, continue without it

        return api_key

    def get_weather_data(self, city: str, units: str = "metric") -> Tuple[Dict, Optional[str]]:
        """
        Fetch weather data for a given city

        Args:
            city: Name of the city to get weather for
            units: Temperature units ('metric', 'imperial', 'kelvin')

        Returns:
            Tuple of (weather_data_dict, error_message)
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': units
        }

        try:
            response = requests.get(self.BASE_URL, params=params)

            if response.status_code == 200:
                return response.json(), None
            elif response.status_code == 404:
                return {}, "City not found"
            elif response.status_code == 401:
                return {}, "Invalid API key"
            elif response.status_code == 429:
                return {}, "API rate limit exceeded"
            else:
                return {}, f"API request failed with status code: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return {}, "No internet connection"
        except requests.exceptions.Timeout:
            return {}, "Request timed out"
        except requests.exceptions.RequestException as e:
            return {}, f"Request error: {str(e)}"
        except Exception as e:
            return {}, f"Unexpected error: {str(e)}"

    def get_weather_by_coordinates(self, lat: float, lon: float, units: str = "metric") -> Tuple[Dict, Optional[str]]:
        """
        Fetch weather data for given coordinates

        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature units ('metric', 'imperial', 'kelvin')

        Returns:
            Tuple of (weather_data_dict, error_message)
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units
        }

        try:
            response = requests.get(self.BASE_URL, params=params)

            if response.status_code == 200:
                return response.json(), None
            elif response.status_code == 401:
                return {}, "Invalid API key"
            elif response.status_code == 429:
                return {}, "API rate limit exceeded"
            else:
                return {}, f"API request failed with status code: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return {}, "No internet connection"
        except requests.exceptions.Timeout:
            return {}, "Request timed out"
        except requests.exceptions.RequestException as e:
            return {}, f"Request error: {str(e)}"
        except Exception as e:
            return {}, f"Unexpected error: {str(e)}"


def format_temperature(temp: float, units: str) -> str:
    """
    Format temperature with appropriate unit symbol

    Args:
        temp: Temperature value
        units: Unit system ('metric', 'imperial', 'kelvin')

    Returns:
        Formatted temperature string
    """
    if units == "metric":
        return f"{round(temp)}°C"
    elif units == "imperial":
        return f"{round(temp)}°F"
    else:  # kelvin
        return f"{round(temp)}K"


def get_weather_icon(weather_main: str) -> str:
    """
    Get appropriate weather icon based on weather condition

    Args:
        weather_main: Main weather condition (e.g., 'Clear', 'Clouds', 'Rain')

    Returns:
        Path to appropriate weather icon
    """
    icon_mapping = {
        'Clear': 'sun.png',
        'Clouds': 'clouds.png',
        'Rain': 'rain.png',
        'Drizzle': 'drizzle.png',
        'Thunderstorm': 'thunderstorm.png',
        'Snow': 'snow.png',
        'Mist': 'mist.png',
        'Fog': 'fog.png',
        'Haze': 'haze.png',
        'Smoke': 'smoke.png',
        'Dust': 'dust.png',
        'Sand': 'sand.png',
        'Ash': 'ash.png',
        'Squall': 'squall.png',
        'Tornado': 'tornado.png'
    }

    return icon_mapping.get(weather_main, 'unknown.png')


def get_background_color(weather_main: str) -> str:
    """
    Get appropriate background color based on weather condition

    Args:
        weather_main: Main weather condition (e.g., 'Clear', 'Clouds', 'Rain')

    Returns:
        Hex color code for background
    """
    color_mapping = {
        'Clear': '#87CEEB',      # Sky blue
        'Clouds': '#B0C4DE',     # Light steel blue
        'Rain': '#708090',       # Slate gray
        'Drizzle': '#708090',    # Slate gray
        'Thunderstorm': '#2F4F4F', # Dark slate gray
        'Snow': '#F0F8FF',       # Alice blue
        'Mist': '#E6E6FA',       # Lavender
        'Fog': '#E6E6FA',        # Lavender
        'Haze': '#F5F5DC',       # Beige
        'Smoke': '#7C7C7C',      # Gray
        'Dust': '#D2B48C',       # Tan
        'Sand': '#F4A460',       # Sandy brown
        'Ash': '#969696',        # Medium gray
        'Squall': '#696969',     # Dim gray
        'Tornado': '#778899'     # Light slate gray
    }

    return color_mapping.get(weather_main, '#F0F0F0')  # Default light gray