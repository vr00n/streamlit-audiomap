import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import random
from pydub import AudioSegment
import time

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

# Function to create a Folium map with markers
def create_map(data):
    start_location = (data[0]['latitude'], data[0]['longitude'])
    m = folium.Map(location=start_location, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)
    for point in data:
        folium.Marker(location=(point['latitude'], point['longitude']), popup=f"Timestamp: {point['timestamp']}s").add_to(marker_cluster)
    return m

# Display audio player
st.audio(audio_path, format='audio/mp3')

# Play button functionality
def play_saunter(data):
    for index, point in enumerate(data):
        # Redraw the map with only part of the data up to the current index
        partial_map = create_map(data[:index+1])
        st_folium(partial_map, width=725, height=500)
        # Delay to simulate passing time, adjust delay as necessary
        time.sleep(5)

# Button to start the playback simulation
if st.button('Play Saunter'):
    play_saunter(saunter_data)
