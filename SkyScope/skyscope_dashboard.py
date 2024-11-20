import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import numpy as np
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

class Skylitics:

    def __init__(self):
        self.location = None
        self.api_key = 'API Key'
        self.url = 'http://api.openweathermap.org/data/2.5/forecast'
        self.params = {
            'appid': self.api_key,
            'units': 'metric'
        }
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    
    def weather_data(self):
        if self.location:
            self.params['q'] = self.location

        response = requests.get(self.url, self.params)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Failed to fetch weather data. Status Code: {response.status_code}")
            return None

        if not data:
            print("No weather data available.")
            return None

        current_date = datetime.utcnow().date()
        forecast_days = [current_date, current_date + timedelta(days=1), current_date + timedelta(days=2)]

        daily_forecasts = {}
        for item in data['list']:
            forecast_time = datetime.utcfromtimestamp(item['dt'])
            forecast_date = forecast_time.date()

            if forecast_date in forecast_days and forecast_date not in daily_forecasts:
                daily_forecasts[forecast_date] = item

        return daily_forecasts

    def create_plots(self, daily_forecasts):
        dates = []
        temps = []
        humidities = []
        pressures = []
        directions = []
        speeds = []
        precip_probs = []
        weather_conditions = {}

        for forecast_date, forecast in daily_forecasts.items():
            dates.append(forecast_date.strftime('%A, %d %B %Y'))
            temps.append(forecast['main']['temp'])
            humidities.append(forecast['main']['humidity'])
            pressures.append(forecast['main']['pressure'])
            directions.append(forecast['wind']['deg'])
            speeds.append(forecast['wind']['speed'])
            precip_probs.append(forecast.get('pop', 0) * 100)
            condition = forecast['weather'][0]['description']
            weather_conditions[condition] = weather_conditions.get(condition, 0) + 1

        # Bar Chart
        bar_chart = go.Figure(data=[
            go.Bar(name='Temperature (°C)', x=dates, y=temps, marker_color='blue'),
            go.Bar(name='Humidity (%)', x=dates, y=humidities, marker_color='orange')
        ])
        bar_chart.update_layout(
            title="Temperature and Humidity for the Next 3 Days",
            barmode='group',
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark"
        )

        # Pie Chart
        pie_chart = go.Figure(data=[go.Pie(labels=list(weather_conditions.keys()), values=list(weather_conditions.values()))])
        pie_chart.update_layout(title="Weather Condition Distribution for the Next 3 Days")

        # Gauge Chart
        current_humidity = daily_forecasts[list(daily_forecasts.keys())[0]]['main']['humidity']
        gauge_chart = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_humidity,
            title={'text': "Current Humidity (%)"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "blue"}}
        ))

        # Box Plot
        box_plot = go.Figure(data=[go.Box(y=temps, boxmean=True)])
        box_plot.update_layout(title="Temperature Variability for the Next 3 Days", yaxis_title="Temperature (°C)")

        # Heatmap
        heatmap_data = np.array([temps, humidities])
        heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=dates,
            y=["Temperature (°C)", "Humidity (%)"],
            colorscale='Viridis'
        ))
        heatmap.update_layout(title="Temperature and Humidity Heatmap for the Next 3 Days")

        # Polar Bar Chart for Wind Speed and Direction
        polar_chart = go.Figure(
            data=go.Barpolar(
                r=speeds,
                theta=directions,
                width=[15] * len(speeds),
                marker_color=speeds,
                marker_colorscale='Blues',
                opacity=0.75
            )
        )
        polar_chart.update_layout(
            title="Wind Speed and Direction",
            polar=dict(
                angularaxis=dict(direction="clockwise", showline=False),
                radialaxis=dict(angle=45, gridcolor="gray")
            )
        )
    
        # Line Chart for Atmospheric Pressure
        pressure_chart = go.Figure(
            data=go.Scatter(
                x=dates,
                y=pressures,
                mode='lines+markers',
                line=dict(color='purple')
            )
        )
        pressure_chart.update_layout(
            title="Atmospheric Pressure Over the Next 3 Days",
            xaxis_title="Date",
            yaxis_title="Pressure (hPa)",
            template="plotly_dark"
        )

        # Combined Chart for Precipitation and Temperature
        combined_chart = go.Figure()

        # Add precipitation as a bar chart
        combined_chart.add_trace(go.Bar(
            x=dates,
            y=precip_probs,
            name="Precipitation Probability (%)",
            marker_color='blue',
            yaxis='y1'  # Use primary y-axis
        ))

        # Add temperature as a line chart
        combined_chart.add_trace(go.Scatter(
            x=dates,
            y=temps,
            name="Temperature (°C)",
            mode='lines+markers',
            line=dict(color='orange'),
            yaxis='y2'  # Use secondary y-axis
        ))

        # Update layout for dual y-axis and adjusted title/legend
        combined_chart.update_layout(
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

        return bar_chart, pie_chart, gauge_chart, box_plot, heatmap, polar_chart, pressure_chart, combined_chart
    
    def app_layout(self):
        self.app.layout = html.Div([
            html.H1("Weather Forecast Dashboard", style={'textAlign': 'center'}),
            dcc.Input(id='location-input', type='text', placeholder='Enter location', style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Button(id='submit-button', n_clicks=0, children='Submit', style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(id='forecast-output', style={'textAlign': 'center', 'marginBottom': '20px'}),

            dcc.Graph(id='bar-chart'),
            dcc.Graph(id='pie-chart'),
            dcc.Graph(id='gauge-chart'),
            dcc.Graph(id='box-plot'),
            dcc.Graph(id='heatmap'),
            dcc.Graph(id='polar-chart'),
            dcc.Graph(id='line-chart'),
            dcc.Graph(id='combined-chart')
        ])
    
    def callback(self):
        @self.app.callback(
            [
                dash.dependencies.Output('forecast-output', 'children'),
                dash.dependencies.Output('bar-chart', 'figure'),
                dash.dependencies.Output('pie-chart', 'figure'),
                dash.dependencies.Output('gauge-chart', 'figure'),
                dash.dependencies.Output('box-plot', 'figure'),
                dash.dependencies.Output('heatmap', 'figure'),
                dash.dependencies.Output('polar-chart', 'figure'),
                dash.dependencies.Output('line-chart', 'figure'),
                dash.dependencies.Output('combined-chart', 'figure')
            ],
            [dash.dependencies.Input('submit-button', 'n_clicks')],
            [dash.dependencies.State('location-input', 'value')]
        )
        def update_dashboard(n_clicks, location):
            if n_clicks == 0 or not location:
                return "Please enter a location and click Submit.", {}, {}, {}, {}, {}, {}, {}, {}

            # Set the location dynamically based on user input
            self.location = location
            self.params['q'] = self.location

            # Fetch weather data
            daily_forecasts = self.weather_data()
            if not daily_forecasts:
                return f"No data available for {location}. Please check the location and try again.", {}, {}, {}, {}, {}, {}, {}, {}

            # Generate the plots
            bar_chart, pie_chart, gauge_chart, box_plot, heatmap, polar_chart, line_chart, combined_chart = self.create_plots(daily_forecasts)

            return (
                f"Weather forecast for {location.capitalize()}:",
                bar_chart,
                pie_chart,
                gauge_chart,
                box_plot,
                heatmap,
                polar_chart,
                line_chart,
                combined_chart
            )
    
    def run(self):
        self.app_layout()
        self.callback()
        self.app.run_server(debug=True)

if __name__ == '__main__':
    dashboard = Skylitics()
    dashboard.run()



        