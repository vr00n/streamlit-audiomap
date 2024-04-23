import os
import time
import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_folium import folium_static
import folium

# Set up session state
if "recording" not in st.session_state:
    st.session_state.recording = False
if "locations" not in st.session_state:
    st.session_state.locations = []

# Function to handle recording button click
def start_recording():
    st.session_state.recording = True
    st.session_state.locations = []

# Function to handle stop button click
def stop_recording():
    st.session_state.recording = False
    session_id = datetime.now().strftime("%m%d%Y%H%M%S")
    
    # Save locations to CSV
    locations_df = pd.DataFrame(st.session_state.locations, columns=["Timestamp", "Latitude", "Longitude"])
    locations_df.to_csv(f"{session_id}.csv", index=False)
    
    # Save session file
    with open(f"{session_id}.session", "w") as f:
        f.write(f"{session_id}.csv,{session_id}.mp3")
    
    st.success("Recording stopped and files saved.")

# Function to get current location
def get_location():
    # Placeholder for getting the current location
    # Replace with actual location retrieval logic
    latitude = 40.7128
    longitude = -74.0060
    return latitude, longitude

# Streamlit app
def main():
    st.title("Audio and Location Recorder")
    
    if not st.session_state.recording:
        if st.button("Start Recording"):
            start_recording()
    else:
        if st.button("Stop Recording"):
            stop_recording()
        
        # Get current location
        latitude, longitude = get_location()
        st.session_state.locations.append((time.time(), latitude, longitude))
        
        # Display map with current location
        map_data = folium.Map(location=[latitude, longitude], zoom_start=12)
        folium.Marker(location=[latitude, longitude]).add_to(map_data)
        folium_static(map_data)
    
    # Display recorded locations
    if st.session_state.locations:
        locations_df = pd.DataFrame(st.session_state.locations, columns=["Timestamp", "Latitude", "Longitude"])
        st.write(locations_df)

if __name__ == "__main__":
    main()
