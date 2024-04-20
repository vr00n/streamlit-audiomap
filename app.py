import streamlit as st
from streamlit_folium import st_folium
import folium
import random
from pydub import AudioSegment

# Ensure session state variables are initialized
if 'markers' not in st.session_state:
    st.session_state.markers = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

# Function to generate random locations in New York City
def generate_random_location():
    min_lat, max_lat = 40.477399, 40.917577
    min_lon, max_lon = -74.259090, -73.700272
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_lon, max_lon)
    return latitude, longitude

# Generate saunter data with random locations
def generate_saunter_data(duration, interval=5):
    num_points = int(duration / interval)
    return [{'timestamp': i * interval, 'latitude': latitude, 'longitude': longitude}
            for i, (latitude, longitude) in enumerate(generate_random_location() for _ in range(num_points + 1))]

# Load and prepare audio
audio_path = 'ny-doc.mp3'  # Path to your MP3 file
audio = AudioSegment.from_mp3(audio_path)
duration = len(audio) / 1000  # Convert duration from milliseconds to seconds
saunter_data = generate_saunter_data(duration)

# Function to create and update Folium map
def create_map(center, zoom=12):
    m = folium.Map(location=center, zoom_start=zoom)
    fg = folium.FeatureGroup(name="Markers")
    for point in st.session_state.markers:
        folium.Marker([point['latitude'], point['longitude']], popup=f"Timestamp: {point['timestamp']}s").add_to(fg)
    m.add_child(fg)
    return m

# Display audio player
st.audio(audio_path, format='audio/mp3')

# Map handling
center = (saunter_data[0]['latitude'], saunter_data[0]['longitude']) if saunter_data else (40.7128, -74.0060)
map_object = create_map(center=center)

# Display map using st_folium
map_display = st_folium(map_object, width=700, height=500)

# Function to simulate map and audio playback synchronization
def play_saunter():
    for index in range(st.session_state.current_index, len(saunter_data)):
        st.session_state.markers.append(saunter_data[index])
        map_object = create_map(center=(saunter_data[index]['latitude'], saunter_data[index]['longitude']))
        map_display = st_folium(map_object, width=700, height=500)
        st.session_state.current_index += 1
        st.experimental_rerun()

# Button to start the playback simulation
if st.button('Play Saunter'):
    play_saunter()
