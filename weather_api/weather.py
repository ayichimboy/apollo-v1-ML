# Import Libraries
import streamlit as st             
import numpy as np                   
import pandas as pd                    
import seaborn as sns                   
import matplotlib.pyplot as plt  
import requests    
from dotenv import load_dotenv, find_dotenv   
import os 
   

# Develope the code for the streamlit APP
class ConFigCon:
    API_KEY=os.getenv("OpenWeatherMap_API_key")
    END_POINT=os.getenv("endpoint_api")
    # CITY = input("Name of City 🌞🌤️🌥️: ")
    
def validate_env():
    var_list = [ConFigCon.API_KEY, ConFigCon.END_POINT]
    
    if not all(var_list):
        raise ValueError("Missing Envirionment Variables")
    
    return var_list[0], var_list[1]
    
def url_link(loc, api_key):
    return f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={api_key}&units=metric"

def call_url(input_url):
    api_url = input_url
    response = requests.get(api_url)
    data = response.json()
    current_temp = data.get("main")["temp"]
    feels_like = data.get("main")["feels_like"]
    current_humidity = data.get("main")["humidity"]
    current_pressure = data.get("main")["pressure"]
    current_wind = data.get("wind")["speed"]
    
    response = {
                "Current Temperature": round(current_temp, 3),
                "Temperature Feels Like": round(feels_like, 3),
                "Current Humidity": round(current_humidity, 3),
                "Current Pressure": round(current_pressure, 3),
                "Current Wind Speed": round(current_wind, 3)
                }
    
    return response

# Setup Streamlit App
def setup_ui():
    """Configure Streamlit UI settings"""
    st.set_page_config(
        # page_title="Location Weather App 🌞🌦️⛅🍃",
        page_icon="🌞",
        layout="centered"
    )
    
def user_input():
    
    # location_name = None
    
    with st.container():
        location_name = st.text_input(label="Please Enter Location Name",
                            value=""
                            )
        
        if location_name:
            location_name = location_name.strip().lower()
            st.write("You wrote:",location_name)
        else:
            st.write("Please type a location name above.")
        
    return location_name
        

def ouput_statement(api_results):
    with st.container():
         st.write(api_results)
               
        
# -- Main Application --
def main():

    load_dotenv()
    find_dotenv()
    
    st.title("🌞🌥️ Weather Info Outlet")
    
    # Setup UI
    setup_ui()
    # user_input()
    
    try:
        api_key,_= validate_env()
        loc_name = user_input()
        
        if loc_name and isinstance(loc_name, str) and loc_name.strip(): # if falsy None, "", 0, [], {}
            loc_name = loc_name.lower().strip()
            
            url = url_link(loc_name, api_key)
            results = call_url(url)
            ouput_statement(results)
            
        else:
            st.warning("⚠️ Please Enter a Valid Location Naming Before Proceeding.")
        
    except ValueError as e:
        st.error(f"Configuration error: {str(e)}")
        # st.info("Please check your WeatherApp API credentials in the .env file")
        
    except Exception as e:
        st.error(f"Application error: {e}")
        # st.info("An unexpected error occurred. Please try again later.")
    
if __name__ == "__main__":
    main()