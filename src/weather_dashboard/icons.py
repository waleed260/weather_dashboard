"""
Module for handling weather icons and dynamic visuals.
"""
import os
import requests
from PIL import Image
try:
    from PIL import ImageTk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    ImageTk = None

from urllib.request import urlopen
from io import BytesIO
import tempfile


class WeatherIconManager:
    """
    Class to handle weather icons and dynamic visual elements
    """

    def __init__(self):
        # Mapping of weather conditions to OpenWeatherMap icon codes
        self.icon_mapping = {
            'Clear': ['01d', '01n'],
            'Clouds': ['02d', '02n', '03d', '03n', '04d', '04n'],
            'Rain': ['09d', '09n', '10d', '10n'],
            'Drizzle': ['09d', '09n', '10d', '10n'],
            'Thunderstorm': ['11d', '11n'],
            'Snow': ['13d', '13n'],
            'Mist': ['50d', '50n'],
            'Fog': ['50d', '50n'],
            'Haze': ['50d', '50n']
        }

        # Reverse mapping from icon codes to weather conditions
        self.reverse_icon_mapping = {}
        for condition, codes in self.icon_mapping.items():
            for code in codes:
                self.reverse_icon_mapping[code] = condition

    def get_icon_url(self, icon_code):
        """
        Get the URL for a weather icon based on its code

        Args:
            icon_code: OpenWeatherMap icon code (e.g., '01d', '02n')

        Returns:
            URL string for the icon
        """
        return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

    def download_and_resize_icon(self, icon_code, size=(100, 100)):
        """
        Download and resize a weather icon

        Args:
            icon_code: OpenWeatherMap icon code
            size: Tuple of (width, height) for the resized icon

        Returns:
            Resized PIL Image object
        """
        try:
            icon_url = self.get_icon_url(icon_code)
            response = requests.get(icon_url)
            response.raise_for_status()

            image_data = BytesIO(response.content)
            image = Image.open(image_data)

            # Resize the image
            resized_image = image.resize(size, Image.Resampling.LANCZOS)

            return resized_image
        except Exception as e:
            print(f"Error downloading/resizing icon {icon_code}: {e}")
            return None

    def get_tkinter_photo_image(self, icon_code, size=(100, 100)):
        """
        Get a PhotoImage object suitable for Tkinter

        Args:
            icon_code: OpenWeatherMap icon code
            size: Tuple of (width, height) for the resized icon

        Returns:
            PhotoImage object for Tkinter
        """
        if not TKINTER_AVAILABLE:
            return None

        pil_image = self.download_and_resize_icon(icon_code, size)
        if pil_image:
            return ImageTk.PhotoImage(pil_image)
        return None

    def get_weather_condition_from_icon(self, icon_code):
        """
        Get the weather condition name from an icon code

        Args:
            icon_code: OpenWeatherMap icon code

        Returns:
            Weather condition name (e.g., 'Clear', 'Rain')
        """
        return self.reverse_icon_mapping.get(icon_code, 'Unknown')

    def preload_common_icons(self):
        """
        Preload commonly used icons to improve performance
        """
        common_icons = ['01d', '01n', '02d', '02n', '03d', '03n', '04d', '04n', '09d', '09n', '10d', '10n']
        self.preloaded_icons = {}

        for icon_code in common_icons:
            self.preloaded_icons[icon_code] = self.download_and_resize_icon(icon_code)


def get_weather_icon_based_on_condition(weather_main, is_daytime=True):
    """
    Get an appropriate icon code based on weather condition

    Args:
        weather_main: Main weather condition (e.g., 'Clear', 'Clouds', 'Rain')
        is_daytime: Boolean indicating if it's day or night

    Returns:
        OpenWeatherMap icon code
    """
    # Determine if it's day or night based on icon code suffix
    suffix = 'd' if is_daytime else 'n'

    # Map weather condition to icon code
    condition_to_icon = {
        'Clear': f'01{suffix}',
        'Clouds': f'03{suffix}',  # Scattered clouds
        'Rain': f'10{suffix}',
        'Drizzle': f'09{suffix}',
        'Thunderstorm': f'11{suffix}',
        'Snow': f'13{suffix}',
        'Mist': f'50{suffix}',
        'Fog': f'50{suffix}',
        'Haze': f'50{suffix}'
    }

    return condition_to_icon.get(weather_main, f'01{suffix}')  # Default to clear sky