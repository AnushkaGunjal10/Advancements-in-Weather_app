import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np

# OpenWeatherMap API Key (Replace with your own key)
API_KEY = "5240efa02cc404a048b1413c92d1786c"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Adding a background image
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1522565810999-fac44acbcf56');
        background-size: cover;
        background-position: center;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather(city, units='metric'):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# Add a sidebar for extra controls
st.sidebar.title("Settings")
unit_choice = st.sidebar.radio("Choose temperature unit:", ("Celsius", "Fahrenheit"))

# Convert units based on user selection
unit = 'metric' if unit_choice == 'Celsius' else 'imperial'

st.title("🌤️ Real-Time Weather App")

city = st.text_input("🏙️ Enter city name:")
if st.button("🔍 Get Weather"):
    if city:
        data = get_weather(city, units=unit)
        if data["cod"] == 200:
            st.success(f"🌍 Weather in {city.capitalize()}:")
            temp_unit = "°C" if unit == 'metric' else "°F"
            st.write(f"🌡️ Temperature: {data['main']['temp']} {temp_unit}")
            st.write(f"☁️ Weather: {data['weather'][0]['description'].capitalize()}")
            st.write(f"💧 Humidity: {data['main']['humidity']}%")
            st.write(f"🌬️ Wind Speed: {data['wind']['speed']} m/s")
            st.write(f"🌅 Sunrise: {datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')}")
            st.write(f"🌇 Sunset: {datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')}")
            
            # Adding Weather Icon
            icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            st.image(icon_url, width=100)
            
            # Plotting a simple graph of temperature throughout the day
            times = ['6 AM', '12 PM', '6 PM', '12 AM']
            temps = [data['main']['temp'], data['main']['temp'] + 2, data['main']['temp'] + 4, data['main']['temp'] - 1]
            
            fig, ax = plt.subplots()
            ax.plot(times, temps, marker='o', color='blue', linestyle='-', linewidth=2, markersize=8)
            ax.set_title('Temperature throughout the Day')
            ax.set_xlabel('Time')
            ax.set_ylabel(f'Temperature ({temp_unit})')
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.error("❌ City not found. Please enter a valid city name.")
    else:
        st.warning("⚠️ Please enter a city name.")
