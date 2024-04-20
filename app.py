import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import random
from pydub import AudioSegment
import time

# Initialize session state for map properties if not already set
if 'zoom' not in st.session_state:
    st.session_state['zoom'] = 12  # Initial zoom level
if 'center' not in st.session_state:
    st.session_state['center'] = (40.7128, -74.0060)  # Initial center of the map (New York City)
if 'markers' not in st.session_state:
    st.session_state['markers'] = []  # List to store markers

# Function to generate random locations in New York City
def generate_random_location():
    min_lat, max_lat = 40.477399, 40.917577
    min_lon, max_lon = -74.259090, -73.700272
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_lon, max_lon)
    return latitude, longitude

# Generate saunter data with random locations
def generate_saunter_data(duration, interval=5):
    num_points = int(duration / interval)  # Generate a point every 5 seconds
    return [{'timestamp': i * interval, 'latitude': latitude, 'longitude': longitude}
            for i, (latitude, longitude) in enumerate(generate_random_location() for _ in range(num_points + 1))]

# Load and prepare audio
audio_path = 'ny-doc.mp3'  # Update with the path to your audio file

# Use pydub to determine the length of the audio file in seconds
audio = AudioSegment.from_mp3(audio_path)
duration = len(audio) / 1000  # duration in seconds

# Generate data based on actual audio duration
saunter_data = generate_saunter_data(duration)

# Display audio player
st.audio(audio_path, format='audio/mp3')

# Initial Map Setup
m = folium.Map(location=st.session_state['center'], zoom_start=st.session_state['zoom'])
fg = folium.FeatureGroup(name="My Map")

# Function to update the map dynamically
def update_map(data):
    for index, point in enumerate(data):
        marker = folium.Marker([point['latitude'], point['longitude']], popup=f"Timestamp: {point['timestamp']}s")
        fg.add_child(marker)
        st.session_state['markers'].append(marker)
        st.session_state['center'] = (point['latitude'], point['longitude'])
        st_folium(m, center=st.session_state['center'], zoom=st.session_state['zoom'], feature_group_to_add=fg, height=400, width=700)
        time.sleep(5)  # Delay to simulate time passage

# Button to start the playback simulation
if st.button('Play Saunter'):
    update_map(saunter_data)
