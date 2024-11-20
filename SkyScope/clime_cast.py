import requests
from datetime import datetime, timedelta

class Skylitics:

    def __init__(self):
        self.location = input("Enter the location for weather forecast: ")
        self.api_key = 'API Key'
        self.url = 'http://api.openweathermap.org/data/2.5/forecast'
        self.params = {
            'q': self.location,
            'appid': self.api_key,
            'units': 'metric'  # Use 'metric' for Celsius, 'imperial' for Fahrenheit
        }
    
    def weather_data(self):
        response = requests.get(self.url, self.params)
        if response.status_code == 200:
            data = response.json()
        else:
            print("Failed to fetch weather data.")
            return  # Exit if request failed
        
        if not data:
            print("No weather data available.")
            return  # Exit if no data available
        
        # Extracting today and next two days' weather data
        print(f"Weather forecast for {data['city']['name']}, {data['city']['country']}:\n")

        current_date = datetime.utcnow().date()
        forecast_days = [current_date, current_date + timedelta(days=1), current_date + timedelta(days=2)]

        # Filter forecast data to get the first instance of each day
        daily_forecasts = {}
        for item in data['list']:
            forecast_time = datetime.utcfromtimestamp(item['dt'])
            forecast_date = forecast_time.date()
        
            # Store only one forecast per day (the first occurrence)
            if forecast_date in forecast_days and forecast_date not in daily_forecasts:
                daily_forecasts[forecast_date] = item

        # Print the detailed weather forecast
        for forecast_date, forecast in daily_forecasts.items():
            date_str = forecast_date.strftime('%A, %d %B %Y')
            temp = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            description = forecast['weather'][0]['description'].capitalize()
            wind_speed = forecast['wind']['speed']
            wind_direction = forecast['wind']['deg']
            pressure = forecast['main']['pressure']
            precipitation = forecast.get('pop', 0) * 100  # Precipitation probability (0 to 1)

            print(f"{date_str}:")
            print(f"  Temperature: {temp}°C")
            print(f"  Humidity: {humidity}%")
            print(f"  Weather: {description}")
            print(f"  Wind: {wind_speed} m/s, {wind_direction}°")
            print(f"  Atmospheric Pressure: {pressure} hPa")
            print(f"  Precipitation Probability: {precipitation}%")
            print()  # Blank line for readability

if __name__ == '__main__':
    forecast = Skylitics()
    forecast.weather_data()
