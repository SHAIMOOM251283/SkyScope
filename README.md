# SkyScope

## Overview

**SkyScope** is a Python-based project designed to provide weather-related data insights, visualizations, and dashboards. It consists of three independent scripts:

1. **clime_cast.py**: Fetches weather forecast data and prints the extracted data to the terminal.
2. **clime_charts.py**: Visualizes the forecast data using Plotly for interactive charts.
3. **skyscope_dashboard.py**: A dashboard that combines the functionalities of the other two scripts to provide a dynamic user interface for displaying weather data and visualizations.

Each script is modular and can be used independently, offering flexible solutions for exploring and presenting weather forecasts.

## Features

- **Data Extraction with API**: Fetches weather forecast data from a public API.
- **Interactive Visualizations**: Generates interactive visualizations using Plotly for weather data.
- **Real-time Dashboard**: Displays a fully interactive dashboard for real-time weather monitoring.
- **Modular and User-Friendly Code**: User-friendly and modular code that can be used independently or as a whole.
- **Weather Parameters Visualization**: Provides visual representation of key weather parameters like temperature, humidity, and precipitation.

## Installation

### Step 1: Clone the Repository

You have multiple options to clone the repository based on your preference:

#### Option 1: Using the Terminal
1. Open a terminal window.
2. Run the following commands:

   ```bash
   git clone https://github.com/SHAIMOOM251283/Skycope.git
   cd SkyScope
   ```

#### Option 2: Using VS Code's Git Integration
1. Open **Visual Studio Code**.
2. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) to open the Command Palette.
3. Type **Git: Clone** and select it.
4. Enter the repository URL:

   ```
   https://github.com/SHAIMOOM251283/SkyScope.git
   ```

5. Choose a local folder to clone the repository into, then select **Open** to load the repository in VS Code.

#### Option 3: Using VS Code's Integrated Terminal
1. Open **VS Code**.
2. Open the integrated terminal by pressing `Ctrl + ` (backtick) or by navigating to **Terminal > New Terminal**.
3. Run the following commands in the integrated terminal:

   ```bash
   git clone https://github.com/SHAIMOOM251283/SkyScope.git
   cd SkyScope
   ```

### Step 2: Set Up the Python Environment and Install Dependencies

Ensure you have Python installed (preferably version 3.8 or later).

1. **Create a Virtual Environment** (recommended for isolated dependencies):
   
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

3. **Install Required Packages**:

   Run the following command to install all necessary packages:

   ```bash
   pip install -r requirements.txt
   ```

   The project explicitly depends on the following libraries:
   - `requests`
   - `plotly`
   - `numpy`
   - `dash`
   - `dash-bootstrap-components`

### Step 3: Verify Installation in VS Code

1. **Open the Project Folder**:
   - In VS Code, go to `File > Open Folder`, and select the `sky-scope` directory.

2. **Select Python Interpreter**:
   - Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) to open the Command Palette.
   - Type **Python: Select Interpreter** and select the interpreter from the `.venv` directory created in Step 2.

## Usage

Before running the scripts, you need to obtain an API key from OpenWeatherMap. Follow these steps:

    Sign up or log in to OpenWeatherMap.
    Generate your API key under the API Keys section in your account dashboard.
    Add the API key to the scripts by replacing the placeholder value.

Once you have the API key and the installation is complete, you can run any of the scripts individually:

- To run the **clime_cast.py** script (weather data fetching):
  
  ```bash
  python clime_cast.py
  ```

- To run the **clime_charts.py** script (visualizations):
  
  ```bash
  python clime_charts.py
  ```

- To run the **skyscope_dashboard.py** script (main dashboard):

  ```bash
  python skyscope_dashboard.py
  ```

The dashboard will open in your default web browser, where you can interact with the data and visualizations.

## Visualizations  

The **SkyScope** project leverages Plotly to deliver engaging, interactive visualizations that enhance the exploration of weather data:

1. **Bar Chart for Temperature and Humidity**  
   Grouped bar chart visualizing the comparison between daily temperature (°C) and humidity (%) over the next three days, showcasing variations in key weather metrics.  

2. **Pie Chart for Weather Conditions**  
   Pie chart illustrating the breakdown of different weather conditions—clear skies, rain, or clouds—predicted for the next three days.  

3. **Gauge Chart for Humidity Levels**  
   Gauge chart providing a quick, intuitive display of the current humidity percentage, offering a snapshot of atmospheric moisture.  

4. **Box Plot for Temperature Variability**  
   Box plot highlighting temperature variability over the next three days, focusing on the range, median, and potential extremes to uncover trends and patterns.  

5. **Heatmap for Temperature and Humidity**  
   Heatmap visualizing temperature and humidity data for each day, using color intensity to show their magnitudes and provide a comparative view.  

6. **Polar Bar Chart for Wind Speed and Direction**  
   Polar bar chart depicting wind speed and its directional distribution over the next three days, offering a clear understanding of wind patterns.  

7. **Line Chart for Atmospheric Pressure**  
   Line chart illustrating atmospheric pressure (hPa) trends across the next three days, with markers and smooth curves for enhanced clarity.  

8. **Combined Chart for Precipitation Probability and Temperature**  
   Dual-axis chart overlaying precipitation probability (bars) and temperature (line), providing a comprehensive view of their relationship over the next three days.  

These visualizations offer detailed insights into weather data, transforming forecasts into actionable intelligence for better decision-making.

## Dashboard Functionality Demonstration
Watch the video to see the dashboard in action: [Dashboard Screencast](https://github.com/SHAIMOOM251283/SkyScope/blob/main/DashboardScreencast.mp4)

## Project Highlights  

- **Modular Design**: The project is structured into three independent scripts that can function independently or seamlessly integrate for enhanced functionality.  
- **Comprehensive Visualizations**: Features eight distinct and interactive visualizations, including bar charts, pie charts, heatmaps, and dual-axis charts, catering to diverse analytical needs.  
- **Real-time Weather Data**: Integrates with a public weather API to fetch the latest three-day weather forecasts, ensuring accurate and timely data.  
- **Interactive and Intuitive Visualizations**: Built with Plotly, the visualizations are fully interactive, allowing users to hover, zoom, and pan for detailed exploration.  
- **Dynamic Web Interface with Dash**: The **SkyScope Dashboard** leverages Dash, a Python framework for building web applications, to present the data through a clean, responsive, and interactive user interface.  
- **User-Friendly Interface**: The dashboard is simple and intuitive, designed for accessibility across all levels of technical expertise.  
- **Insightful Data Representation**: Incorporates advanced chart types, such as polar bar charts and gauge charts, to present data in innovative and meaningful ways.  
- **Versatile Use Cases**: Ideal for professionals, hobbyists, and educators looking to analyze or teach weather data trends interactively.  

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
