import streamlit as st
import requests
import folium
from streamlit_folium import folium_static


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except Exception as e:
        st.error(f"Failed to retrieve public IP: {e}")
        return None


def get_geolocation(ip_address):
    # Replace 'your_api_key' with your actual API key from IPGeolocation
    api_key = '649b40303e344d088d99d72481de8ae7'
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}'
    response = requests.get(url)
    data = response.json()
    return data


def create_map(data, ip_address_v4):
    latitude = data['latitude']
    longitude = data['longitude']

    # Create map centered around the location with adjusted zoom level
    # Adjust zoom level here
    map_obj = folium.Map(location=[latitude, longitude], zoom_start=10)

    # Construct popup HTML with location and IP address information
    popup_html = f"<b>Your Location:</b><br>Latitude: {latitude}<br>Longitude: {longitude}<br>City: {data['city']}<br>Country: {data['country_name']}<br>IP Address (IPv4): {ip_address_v4}"

    # Add marker with popup
    folium.Marker([latitude, longitude], popup=popup_html).add_to(map_obj)

    # Render map in Streamlit
    folium_static(map_obj)


def main():
    st.title("Geolocation Tracker")

    ip_address_v4 = get_public_ip()
    if ip_address_v4:
        st.write(f"Your public IPv4 address: {ip_address_v4}")
        location_data = get_geolocation(ip_address_v4)
        create_map(location_data, ip_address_v4)
    else:
        st.error("Failed to retrieve public IPv4 address.")


if __name__ == "__main__":
    main()
