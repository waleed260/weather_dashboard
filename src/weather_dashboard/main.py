"""
Main entry point for the Weather Dashboard application.
"""
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    TKINTER_AVAILABLE = True
    from PIL import Image, ImageTk
except ImportError:
    TKINTER_AVAILABLE = False
    tk = None
    ttk = None
    messagebox = None
    ImageTk = None

import os
from PIL import Image
from .api import WeatherAPI, format_temperature, get_background_color
from .icons import WeatherIconManager, get_weather_icon_based_on_condition

class WeatherDashboard:
    def __init__(self):
        if not TKINTER_AVAILABLE:
            print("Error: tkinter is not available. Please install tkinter for your Python distribution.")
            print("On Ubuntu/Debian: sudo apt-get install python3-tk")
            print("On CentOS/RHEL: sudo yum install tkinter or sudo dnf install python3-tkinter")
            print("On macOS with Homebrew: brew install python-tk")
            raise RuntimeError("tkinter is required but not available")

        self.root = tk.Tk()
        self.root.title("Atmosphere - Dynamic Weather Dashboard")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Initialize API
        try:
            self.weather_api = WeatherAPI()
        except ValueError as e:
            messagebox.showerror("API Error", str(e))
            # We'll still continue but with limited functionality
            self.weather_api = None

        # Initialize units (default to Celsius)
        self.units = "metric"  # "metric" for Celsius, "imperial" for Fahrenheit

        # Initialize icon manager
        self.icon_manager = WeatherIconManager()

        # Weather condition mapping for icons
        self.weather_icons = {}
        self.load_weather_icons()

        # Create the UI
        self.setup_ui()

    def load_weather_icons(self):
        """Load weather condition icons"""
        # This will be implemented to load appropriate icons based on weather conditions
        # For now, we'll just note that this functionality is planned
        pass

    def setup_ui(self):
        """Initialize the user interface"""
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Main container frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)

        title_label = ttk.Label(
            header_frame,
            text="Atmosphere - Dynamic Weather Dashboard",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0)

        # Search section
        search_frame = ttk.LabelFrame(main_frame, text="Search Location", padding="10")
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        search_frame.columnconfigure(0, weight=1)

        # Search input
        search_input_frame = ttk.Frame(search_frame)
        search_input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        search_input_frame.columnconfigure(0, weight=1)

        self.city_entry = ttk.Entry(search_input_frame, font=("Arial", 12))
        self.city_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.city_entry.bind('<Return>', lambda event: self.search_weather())

        search_button = ttk.Button(
            search_input_frame,
            text="Search",
            command=self.search_weather
        )
        search_button.grid(row=0, column=1)

        # Units toggle
        units_frame = ttk.Frame(search_frame)
        units_frame.grid(row=1, column=0, pady=(10, 0), sticky=(tk.W))

        self.units_var = tk.StringVar(value="Celsius")
        celsius_radio = ttk.Radiobutton(
            units_frame,
            text="Celsius (°C)",
            variable=self.units_var,
            value="Celsius",
            command=self.toggle_units
        )
        fahrenheit_radio = ttk.Radiobutton(
            units_frame,
            text="Fahrenheit (°F)",
            variable=self.units_var,
            value="Fahrenheit",
            command=self.toggle_units
        )
        celsius_radio.grid(row=0, column=0, sticky=tk.W)
        fahrenheit_radio.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        # Weather display section
        self.weather_frame = ttk.LabelFrame(main_frame, text="Weather Information", padding="15")
        self.weather_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.weather_frame.columnconfigure(0, weight=1)

        # Placeholder for weather data
        self.placeholder_label = ttk.Label(
            self.weather_frame,
            text="Enter a city name to get weather information",
            font=("Arial", 12),
            foreground="#666666"
        )
        self.placeholder_label.grid(row=0, column=0)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

    def toggle_units(self):
        """Toggle between Celsius and Fahrenheit"""
        if self.units_var.get() == "Celsius":
            self.units = "metric"
        else:
            self.units = "imperial"

        # If we have current weather data, refresh it with new units
        current_city = getattr(self, 'current_city', None)
        if current_city:
            self.get_weather(current_city)

    def search_weather(self):
        """Handle the search button click"""
        city = self.city_entry.get().strip()
        if city:
            self.get_weather(city)
        else:
            messagebox.showwarning("Input Error", "Please enter a city name")

    def get_weather(self, city):
        """Fetch weather data from OpenWeatherMap API"""
        if not self.weather_api:
            messagebox.showerror("API Error", "Weather API is not properly configured")
            return

        try:
            self.status_var.set(f"Fetching weather for {city}...")

            data, error = self.weather_api.get_weather_data(city, self.units)

            if error:
                if "City not found" in error:
                    messagebox.showerror("City Not Found", f"City '{city}' not found")
                    self.clear_weather_display()
                elif "No internet connection" in error:
                    messagebox.showerror("Connection Error", "No internet connection available")
                    self.clear_weather_display()
                else:
                    messagebox.showerror("API Error", f"Error fetching weather data: {error}")
                    self.clear_weather_display()
            else:
                self.display_weather(data)
                self.current_city = city

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.clear_weather_display()
        finally:
            self.status_var.set("Ready")

    def display_weather(self, data):
        """Display weather information in the UI"""
        # Clear placeholder if present
        for widget in self.weather_frame.winfo_children():
            if widget != self.placeholder_label:
                widget.destroy()

        # Extract data
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        weather_main = data['weather'][0]['main']

        # Get the icon code from the API response
        icon_code = data['weather'][0]['icon']

        # Format temperature
        temp_text = format_temperature(temp, self.units)
        feels_like_text = format_temperature(feels_like, self.units)

        # Create weather display
        # City header
        city_header = ttk.Label(
            self.weather_frame,
            text=f"{city_name}, {country}",
            font=("Arial", 16, "bold")
        )
        city_header.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky=tk.W)

        # Weather icon
        try:
            # Try to get the icon from the API response
            icon_photo = self.icon_manager.get_tkinter_photo_image(icon_code, (80, 80))
            if icon_photo:
                icon_label = ttk.Label(self.weather_frame, image=icon_photo)
                icon_label.image = icon_photo  # Keep a reference to prevent garbage collection
                icon_label.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)
        except Exception as e:
            # If there's an error getting the icon, continue without it
            print(f"Error loading weather icon: {e}")

        # Temperature
        temp_frame = ttk.Frame(self.weather_frame)
        temp_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 20))

        temp_label = ttk.Label(
            temp_frame,
            text=temp_text,
            font=("Arial", 36, "bold")
        )
        temp_label.grid(row=0, column=0, sticky=tk.W)

        feels_like_label = ttk.Label(
            temp_frame,
            text=f"Feels like {feels_like_text}",
            font=("Arial", 10)
        )
        feels_like_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        # Weather details
        details_frame = ttk.Frame(self.weather_frame)
        details_frame.grid(row=1, column=2, sticky=(tk.W, tk.E))

        desc_label = ttk.Label(
            details_frame,
            text=description,
            font=("Arial", 12)
        )
        desc_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        humidity_label = ttk.Label(
            details_frame,
            text=f"Humidity: {humidity}%",
            font=("Arial", 12)
        )
        humidity_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 5))

        # Update background based on weather condition
        self.update_background(weather_main)

        # Update status
        self.status_var.set(f"Weather data updated for {city_name}")

    def update_background(self, weather_condition):
        """Update the background based on weather condition"""
        bg_color = get_background_color(weather_condition)

        # Update the style
        style = ttk.Style()
        style.configure('Weather.TLabelframe', background=bg_color)
        style.configure('Weather.TLabel', background=bg_color)

        # Apply the style to the frame
        self.weather_frame.configure(style='Weather.TLabelframe')

        # Also update child widgets to inherit the background
        for widget in self.weather_frame.winfo_children():
            if isinstance(widget, (ttk.Label, ttk.Button, ttk.Radiobutton)):
                widget.configure(style='Weather.TLabel')

    def clear_weather_display(self):
        """Clear the weather display area"""
        # Hide the placeholder if it's currently showing
        self.placeholder_label.grid_remove()

        # Remove all weather display widgets except the placeholder
        for widget in self.weather_frame.winfo_children():
            if widget != self.placeholder_label:
                widget.destroy()

        # Show placeholder again
        self.placeholder_label.grid(row=0, column=0)

    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    app = WeatherDashboard()
    app.run()

if __name__ == "__main__":
    main()