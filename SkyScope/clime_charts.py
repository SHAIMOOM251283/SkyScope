import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np

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
            return

        if not data:
            print("No weather data available.")
            return
        
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

        # Call plotting functions
        self.plot_bar_chart(daily_forecasts)
        self.plot_pie_chart(daily_forecasts)
        self.plot_gauge_chart(daily_forecasts)
        self.plot_box_plot(daily_forecasts)
        self.plot_heatmap(daily_forecasts)
        self.plot_wind_polar(daily_forecasts)
        self.plot_pressure_line(daily_forecasts)
        self.plot_combined_chart(daily_forecasts)
        
    # 1. Bar Chart for Temperature and Humidity
    def plot_bar_chart(self, daily_forecasts):
        dates = []
        temps = []
        humidities = []

        for forecast_date, forecast in daily_forecasts.items():
            dates.append(forecast_date.strftime('%A, %d %B %Y'))
            temps.append(forecast['main']['temp'])
            humidities.append(forecast['main']['humidity'])

        fig = go.Figure(data=[
            go.Bar(name='Temperature (°C)', x=dates, y=temps, marker_color='blue'),
            go.Bar(name='Humidity (%)', x=dates, y=humidities, marker_color='orange')
        ])

        fig.update_layout(
            title="Temperature and Humidity for the Next 3 Days",
            barmode='group',
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark"
        )

        fig.show()

    # 2. Pie Chart for Weather Conditions
    def plot_pie_chart(self, daily_forecasts):
        weather_conditions = {}

        for forecast_date, forecast in daily_forecasts.items():
            condition = forecast['weather'][0]['description']
            weather_conditions[condition] = weather_conditions.get(condition, 0) + 1

        fig = go.Figure(data=[go.Pie(labels=list(weather_conditions.keys()), values=list(weather_conditions.values()))])
        fig.update_layout(title="Weather Condition Distribution for the Next 3 Days")
        fig.show()

    # 3. Gauge Chart for Humidity Levels
    def plot_gauge_chart(self, daily_forecasts):
        current_humidity = daily_forecasts[list(daily_forecasts.keys())[0]]['main']['humidity']

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_humidity,
            title={'text': "Current Humidity (%)"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "blue"}}
        ))

        fig.show()

    # 4. Box Plot for Temperature Variability
    def plot_box_plot(self, daily_forecasts):
        temps = [forecast['main']['temp'] for forecast in daily_forecasts.values()]

        fig = go.Figure(data=[go.Box(y=temps, boxmean=True)])
        fig.update_layout(title="Temperature Variability for the Next 3 Days", yaxis_title="Temperature (°C)")
        fig.show()

    # 5. Heatmap for Temperature and Humidity
    def plot_heatmap(self, daily_forecasts):
        dates = list(daily_forecasts.keys())
        temps = [forecast['main']['temp'] for forecast in daily_forecasts.values()]
        humidities = [forecast['main']['humidity'] for forecast in daily_forecasts.values()]

        # Create the heatmap matrix (rows = days, cols = temp and humidity)
        data = np.array([temps, humidities])

        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=dates,
            y=["Temperature (°C)", "Humidity (%)"],
            colorscale='Viridis'
        ))

        fig.update_layout(title="Temperature and Humidity Heatmap for the Next 3 Days")
        fig.show()
    
    # 6. Polar Bar Chart for Wind Speed and Direction
    def plot_wind_polar(self, daily_forecasts):
        directions = []
        speeds = []

        for forecast_date, forecast in daily_forecasts.items():
            directions.append(forecast['wind']['deg'])  # Wind direction in degrees
            speeds.append(forecast['wind']['speed'])    # Wind speed in m/s

        fig = go.Figure(
            data=go.Barpolar(
                r=speeds,
                theta=directions,
                width=[15] * len(speeds),
                marker_color=speeds,
                marker_colorscale='Blues',
                opacity=0.75
            )
        )
        fig.update_layout(
            title="Wind Speed and Direction",
            polar=dict(
                angularaxis=dict(direction="clockwise", showline=False),
                radialaxis=dict(angle=45, gridcolor="gray")
            )
        )
        fig.show()
    
    # 7. Line Chart for Atmospheric Pressure
    def plot_pressure_line(self, daily_forecasts):
        dates = []
        pressures = []

        for forecast_date, forecast in daily_forecasts.items():
            dates.append(forecast_date.strftime('%A, %d %B %Y'))
            pressures.append(forecast['main']['pressure'])

        fig = go.Figure(
            data=go.Scatter(
                x=dates,
                y=pressures,
                mode='lines+markers',
                line=dict(color='purple')
            )
        )
        fig.update_layout(
            title="Atmospheric Pressure Over the Next 3 Days",
            xaxis_title="Date",
            yaxis_title="Pressure (hPa)",
            template="plotly_dark"
        )
        fig.show()
    
    # 8. Plot Precipitation and Temperature
    def plot_combined_chart(self, daily_forecasts):
        dates = []
        temps = []
        precip_probs = []

        for forecast_date, forecast in daily_forecasts.items():
            dates.append(forecast_date.strftime('%A, %d %B %Y'))
            temps.append(forecast['main']['temp'])
            precip_probs.append(forecast.get('pop', 0) * 100)  # Convert precipitation probability to percentage

        fig = go.Figure()

        # Add precipitation as a bar chart
        fig.add_trace(go.Bar(
            x=dates,
            y=precip_probs,
            name="Precipitation Probability (%)",
            marker_color='blue',
            yaxis='y1'  # Use primary y-axis
        ))

        # Add temperature as a line chart
        fig.add_trace(go.Scatter(
            x=dates,
            y=temps,
            name="Temperature (°C)",
            mode='lines+markers',
            line=dict(color='orange'),
            yaxis='y2'  # Use secondary y-axis
        ))

        # Update layout for dual y-axis and adjusted title/legend
        fig.update_layout(
            title=dict(
                text="Precipitation Probability and Temperature Over the Next 3 Days",
                x=0.5,  # Center the title
                y=0.95,  # Position title slightly above
                font=dict(size=20)
            ),
            xaxis_title="Date",
            yaxis_title="Precipitation Probability (%)",
            yaxis=dict(
                title="Precipitation Probability (%)",
                titlefont=dict(color='blue'),
                tickfont=dict(color='blue')
            ),
            yaxis2=dict(
                title="Temperature (°C)",
                titlefont=dict(color='orange'),
                tickfont=dict(color='orange'),
                overlaying='y',  # Overlay secondary axis on primary
                side='right'  # Place secondary axis on the right
            ),
            template="plotly_dark",
            legend=dict(
                x=0.02,  # Position legend near the left
                y=0.85,  # Adjust vertical placement
                bgcolor="rgba(255, 255, 255, 0.1)",  # Semi-transparent background for better visibility
            )
        )

        fig.show()

if __name__ == '__main__':
    forecast = Skylitics()
    forecast.weather_data()
