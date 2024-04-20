import streamlit as st
import json
import time
import numpy as np
from IPython.display import Audio, display, HTML
from ipyleaflet import Map, Marker, Polyline
from ipywidgets import Button, VBox
from pydub import AudioSegment
import random
import requests

# Set page title and header
st.set_page_config(page_title='Saunter Playback', page_icon=':walking:')
st.title('Saunter Playback')

# Function to download the MP3 file from GitHub
def download_mp3(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the MP3 file locally
        with open('audio.mp3', 'wb') as file:
            file.write(response.content)
        
        st.success('MP3 file downloaded successfully!')
    else:
        st.error('Failed to download the MP3 file.')

# Download the MP3 file from the specified GitHub URL
mp3_url = 'https://github.com/vr00n/streamlit-audiomap/raw/main/ny-doc.mp3'
download_mp3(mp3_url)

# Load the downloaded MP3 file
audio_path = 'audio.mp3'
audio = AudioSegment.from_mp3(audio_path)

# Get the duration of the audio in seconds
duration = len(audio) / 1000

# Generate random locations in New York City for the saunter
def generate_random_location():
    # New York City bounding box coordinates
    min_lat, max_lat = 40.477399, 40.917577
    min_lon, max_lon = -74.259090, -73.700272
    
    # Generate random latitude and longitude within the bounding box
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_lon, max_lon)
    
    return latitude, longitude

# Generate saunter data with random locations and timestamps
num_points = int(duration / 5)  # Assuming a point every 5 seconds
saunter_data = []
for i in range(num_points + 1):
    timestamp = i * 5
    latitude, longitude = generate_random_location()
    saunter_data.append({'timestamp': timestamp, 'latitude': latitude, 'longitude': longitude})

# Create a map centered on the starting point of the saunter
map_center = (saunter_data[0]['latitude'], saunter_data[0]['longitude'])
saunter_map = Map(center=map_center, zoom=10)

# Create a Polyline to represent the path
path = Polyline(locations=[], color='blue')
saunter_map.add_layer(path)

# Display the map
st.components.v1.html(saunter_map._repr_html_(), height=400)

# Create an Audio object and display it
audio_widget = Audio(audio_path, autoplay=False)
st.audio(audio_path)

# Function to update the path on the map, center the map, and add a pin
def update_path(index):
    path.locations = [(data['latitude'], data['longitude']) for data in saunter_data[:index+1]]
    saunter_map.center = (saunter_data[index]['latitude'], saunter_data[index]['longitude'])
    
    # Add a pin at the current location
    marker = Marker(location=(saunter_data[index]['latitude'], saunter_data[index]['longitude']))
    saunter_map.add_layer(marker)

# Function to handle audio playback and map synchronization
def play_audio():
    for i in range(len(saunter_data) - 1):
        update_path(i)
        time.sleep(saunter_data[i+1]['timestamp'] - saunter_data[i]['timestamp'])
    
    st.success('Saunter playback completed.')

# Create a button to start the audio and map synchronization
if st.button('Play'):
    play_audio()
