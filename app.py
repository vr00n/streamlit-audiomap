import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import random
from pydub import AudioSegment

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

# Initially create the map with all markers
saunter_map = create_map(saunter_data)

# Display audio player
st.audio(audio_path, format='audio/mp3')

# Display map using st_folium
st_folium(saunter_map, width=725, height=500)

# Button to update the map for demonstration of path
if st.button('Show Path'):
    index = st.session_state.get('index', 0)
    if index < len(saunter_data):
        st.session_state['index'] = index + 1
    # Redraw the map with only part of the data
    partial_map = create_map(saunter_data[:st.session_state['index']])
    st_folium(partial_map, width=725, height=500)
