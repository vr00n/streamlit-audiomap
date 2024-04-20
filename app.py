import streamlit as st
from streamlit_folium import st_folium
import folium
import random
from pydub import AudioSegment

# Initialize session state for markers and index if not already set
if 'markers' not in st.session_state:
    st.session_state['markers'] = []
if 'index' not in st.session_state:
    st.session_state['index'] = 0

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
audio_path = 'ny-doc.mp3'  # Update this path to your audio file
audio = AudioSegment.from_mp3(audio_path)
duration = len(audio) / 1000  # duration in seconds
saunter_data = generate_saunter_data(duration)

# Function to create and update Folium map
def create_map(center, zoom=12):
    m = folium.Map(location=center, zoom_start=zoom)
    fg = folium.FeatureGroup(name="Markers")
    for point in st.session_state['markers']:
        folium.Marker([point['latitude'], point['longitude']], popup=f"Timestamp: {point['timestamp']}s").add_to(fg)
    m.add_child(fg)
    return m

# Display audio player
st.audio(audio_path, format='audio/mp3')

# Display map
if st.session_state['markers']:
    map_center = (st.session_state['markers'][-1]['latitude'], st.session_state['markers'][-1]['longitude'])
else:
    map_center = (40.7128, -74.0060)  # Default center if no markers are present
map_object = create_map(center=map_center)
st_folium(map_object, width=700, height=500)

# Button to move to the next point
if st.button('Next'):
    if st.session_state['index'] < len(saunter_data):
        st.session_state['markers'].append(saunter_data[st.session_state['index']])
        st.session_state['index'] += 1
        st.experimental_rerun()
