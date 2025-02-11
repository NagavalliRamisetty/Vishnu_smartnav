import streamlit as st
import folium
import openrouteservice as ors
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static

# Initialize API clients
geolocator = Nominatim(user_agent='route_finder_app')
client = ors.Client(key='5b3ce3597851110001cf6248c894559991d64d9e8468a0118405dda8')

# Custom places
custom_places = {
    'YUMMY-VISHNU': (16.56862849207908, 81.52216849132942),
    'VIT Boys Canteen':(16.566154802707217, 81.52023292283525),
    
    'BV Raju Park' :(16.567816913381595, 81.52345337500493),
    'Swimming Pool':(16.568363684227528, 81.51955533301734),
    'Canal Gate':(16.567490452313564, 81.52028329695592),
    'Vishnu Sports Complex':(16.56766353608586, 81.5200409315482),
    'Seetha Polytechnic College':(16.569234435424107, 81.52552947651928),
    'B.sc Library':(16.56928301596042, 81.52516623257198),
    'Vishnu Water Plant':(16.569980892659334, 81.52306087166234),
    'Girls Playground':(16.569585165763232, 81.52172971332259),
    'Milk parlour':(16.57005974339694, 81.5226469521092),
    'CS Beauty Parlour':(16.568642341133636, 81.5219827385537),
    'Main Gate':(16.568993709932272, 81.5256739037132),
    'Green Meadows':(16.565917880102532, 81.5202938511844),
    'Vishnu Lake View':(16.5654974634785, 81.52127890692346),
    'South Gate':(16.564822613397382, 81.52211937358457),
}

# Streamlit UI
st.title("🚀 Vishnu SmartNav!")

# Input fields
source = st.text_input("Enter Source Location:")
destination = st.text_input("Enter Destination Location:")

# Find route button
if st.button("Find Route"):
    if source and destination:
        try:
            # Get coordinates
            source_coords = custom_places.get(source, geolocator.geocode(source))
            destination_coords = custom_places.get(destination, geolocator.geocode(destination))

            if not source_coords or not destination_coords:
                st.error("Invalid locations! Please enter valid place names.")
            else:
                source_latlng = (source_coords[0], source_coords[1]) if isinstance(source_coords, tuple) else (source_coords.latitude, source_coords.longitude)
                destination_latlng = (destination_coords[0], destination_coords[1]) if isinstance(destination_coords, tuple) else (destination_coords.latitude, destination_coords.longitude)

                # Request route from OpenRouteService
                coords = [[source_latlng[1], source_latlng[0]], [destination_latlng[1], destination_latlng[0]]]
                route = client.directions(coordinates=coords, profile='foot-walking', format='geojson')

                # Create a folium map
                m = folium.Map(location=source_latlng, zoom_start=18)
                folium.PolyLine(locations=[[p[1], p[0]] for p in route['features'][0]['geometry']['coordinates']], color="red").add_to(m)
                folium.Marker(location=source_latlng, popup=source, icon=folium.Icon(color="blue")).add_to(m)
                folium.Marker(location=destination_latlng, popup=destination, icon=folium.Icon(color="green")).add_to(m)

                # Display the map
                folium_static(m)
        except Exception as e:
            st.error(f"Error: {str(e)}")

