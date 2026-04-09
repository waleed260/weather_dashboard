# Atmosphere: Dynamic Weather Dashboard

A beautiful and functional desktop weather application built with Python and Tkinter that provides real-time weather information with dynamic visuals.

## Features

- Real-time weather data from OpenWeatherMap API
- Search for weather in any city worldwide
- Dynamic background colors based on weather conditions
- Weather icons for visual representation
- Toggle between Celsius and Fahrenheit
- Responsive and modern UI design
- Comprehensive error handling

## Installation


   ```

3. Get an API key from [OpenWeatherMap](https://openweathermap.org/api) (free tier available)

4. Create a `.env` file in the project root with your API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

## Usage

Run the application:
```bash
python -m src.weather_dashboard.main
```

Or if installed as a package:
```bash
weather-dashboard
```

## Configuration

- **API Key**: Store your OpenWeatherMap API key in the `OPENWEATHER_API_KEY` environment variable or in a `.env` file
- **Temperature Units**: Toggle between Celsius and Fahrenheit using the radio buttons in the UI

## Project Structure

```
weather_dashboard/
├── src/
│   └── weather_dashboard/
│       ├── __init__.py
│       ├── main.py          # Main application entry point
│       ├── api.py           # API interaction module
│       └── icons.py         # Weather icon handling
├── pyproject.toml           # Project dependencies and metadata
└── README.md
```

## Dependencies

- Python 3.7+
- requests
- Pillow (PIL)
- python-dotenv (optional, for .env file support)
- tkinter (GUI toolkit - may need separate installation on some systems)


