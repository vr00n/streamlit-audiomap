import streamlit as st
from streamlit_folium import st_folium
import folium
import random
from pydub import AudioSegment

# Initialize session state for map properties if not already set
if 'map_initialized' not in st.session_state:
    st.session_state['map_initialized'] = False
    st.session_state['markers'] = []
    st.session_state['center'] = (40.7128, -74.0060)
    st.session_state['zoom'] = 12

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
audio_path = 'ny-doc.mp3'
audio = AudioSegment.from_mp3(audio_path)
duration = len(audio) / 1000  # in seconds
saunter_data = generate_saunter_data(duration)

def create_map():
    m = folium.Map(location=st.session_state['center'], zoom_start=st.session_state['zoom'])
    fg = folium.FeatureGroup(name="Markers")
    for point in st.session_state['markers']:
        folium.Marker([point['latitude'], point['longitude']], popup=f"Timestamp: {point['timestamp']}s").add_child(fg)
    return m, fg

# Display audio player
st.audio(audio_path, format='audio/mp3')

# Initialize map once
if not st.session_state['map_initialized']:
    m, fg = create_map()
    st.session_state['map_initialized'] = True

# Display map using st_folium
st_folium(m, center=st.session_state['center'], zoom=st.session_state['zoom'], key="new", feature_group_to_add=fg, height=400, width=700)

# Function to update the map dynamically
def play_saunter():
    for point in saunter_data:
        st.session_state['markers'].append(point)
        st.session_state['center'] = (point['latitude'], point['longitude'])
        m, fg = create_map()
        st_folium(m, center=st.session_state['center'], zoom=st.session_state['zoom'], key="new", feature_group_to_add=fg, height=400, width=700)

if st.button('Play Saunter'):
    play_saunter()
