import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

def geocode_location(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['lat'], data[0]['lon']
    return None, None

def get_weather(lat, lon):
    url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(url)
    data = response.json()
    if 'properties' in data:
        forecast_url = data['properties']['forecast']
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        if 'properties' in forecast_data and 'periods' in forecast_data['properties']:
            return forecast_data['properties']['periods'][0]['detailedForecast']
    return "Weather information not available."

st.title("Weather App")
location = st.text_input("Enter a location")

if location:
    lat, lon = geocode_location(location)
    if lat and lon:
        weather = get_weather(lat, lon)
        st.write(f"Weather for {location}:")
        st.write(weather)
    else:
        st.write("Location not found.")