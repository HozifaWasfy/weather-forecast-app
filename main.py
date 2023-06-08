import requests
import json
import argparse
import tkinter as tk
from datetime import datetime, timedelta
from PIL import ImageTk, Image

# OpenWeatherMap API configuration
API_KEY = ""
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ICON_URL = "http://openweathermap.org/img/w/"

# Cache configuration
CACHE_EXPIRATION = timedelta(minutes=10)
cache = {}
cache_timestamps = {}

def fetch_weather_data(city):
    if city in cache and datetime.now() - cache_timestamps[city] < CACHE_EXPIRATION:
        # Return cached data if available and not expired
        return cache[city]
    
    # Fetch weather data from the API
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Update cache with the fetched data
        cache[city] = data
        cache_timestamps[city] = datetime.now()
        
        return data
    else:
        print("Error fetching weather data.")
        return None

def parse_weather_data(data):
    weather = data["weather"][0]["main"]
    description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    
    icon_url = ICON_URL + data["weather"][0]["icon"] + ".png"
    icon = None #ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
    
    return weather, description, temperature, humidity, wind_speed, icon

def fetch_forecast_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(FORECAST_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error fetching forecast data.")
        return None

def parse_forecast_data(data):
    forecast = []
    
    for item in data["list"]:
        timestamp = datetime.fromtimestamp(item["dt"])
        date = timestamp.date()
        weather = item["weather"][0]["main"]
        description = item["weather"][0]["description"]
        temperature = item["main"]["temp"]
        icon_url = ICON_URL + item["weather"][0]["icon"] + ".png"
        icon = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
        
        forecast.append((date, weather, description, temperature, icon))
    
    return forecast

def display_weather_data(city, weather, description, temperature, humidity, wind_speed, icon=None):
    print(f"Weather in {city}: {weather} ({description})")
    print(f"Temperature: {temperature}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print()
    
    if icon:
        root = tk.Tk()
        icon_label = tk.Label(root, image=icon)
        icon_label.pack()
        root.mainloop()

def display_forecast_data(forecast):
    print("Weather Forecast:")
    
    for date, weather, description, temperature, icon in forecast:
        print(f"{date}: {weather} ({description}), {temperature}°C")
        
        root = tk.Tk()
        icon_label = tk.Label(root, image=icon)
        icon_label.pack()
        root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Weather Forecast")
    parser.add_argument("city", help="City name or ZIP code")
    args = parser.parse_args()
    
    city = args.city
    
    weather_data = fetch_weather_data(city)
    if weather_data:
        print(weather_data)
        weather, description, temperature, humidity, wind_speed, _ = parse_weather_data(weather_data)
        display_weather_data(city, weather, description, temperature, humidity, wind_speed)
    
    forecast_data = None #fetch_forecast_data(city)
    if forecast_data:
        forecast = parse_forecast_data(forecast_data)
        display_forecast_data(forecast)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Weather Forecast")
    # parser.add_argument("city", help="City name or ZIP code")
    # args = parser.parse_args()
    
    # city = args.city
    # print(fetch_weather_data(city))
    main()
    
