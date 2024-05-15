# Importing necessary libraries
import streamlit as st  # For building the web app interface
import requests  # For making HTTP requests
import folium  # For creating interactive maps
from streamlit_folium import folium_static  # For integrating Folium maps within Streamlit


def get_public_ip():
    """
    Function to fetch public IPv4 address.

    Returns:
        str: Public IPv4 address.
    """
    try:
        # Fetching public IPv4 address using an external API
        response = requests.get('https://api.ipify.org?format=json')
        data = response.json()
        return data['ip']  # Extracting IPv4 address from the response JSON
    except Exception as e:
        # Displaying error message if fetching fails
        st.error(f"Failed to retrieve public IP: {e}")
        return None


def get_geolocation(ip_address):
    """
    Function to fetch geolocation data using IP address.

    Args:
        ip_address (str): IPv4 address.

    Returns:
        dict: Geolocation data.
    """
    # Replace 'your_api_key' with your actual API key from IPGeolocation
    api_key = 'your_api_key'
    url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_address}'
    response = requests.get(url)
    data = response.json()
    return data


def create_map(data, ip_address_v4):
    """
    Function to create and display map using geolocation data.

    Args:
        data (dict): Geolocation data.
        ip_address_v4 (str): IPv4 address.
    """
    latitude = data['latitude']  # Latitude of the location
    longitude = data['longitude']  # Longitude of the location

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
    """
    Main function to run the Streamlit app.
    """
    st.title("Geolocation Tracker")  # Title of the web app

    # Get public IPv4 address
    ip_address_v4 = get_public_ip()
    if ip_address_v4:
        # Display public IPv4 address
        st.write(f"Your public IPv4 address: {ip_address_v4}")
        # Get geolocation data
        location_data = get_geolocation(ip_address_v4)
        # Create and display map
        create_map(location_data, ip_address_v4)
    else:
        # Display error message if fetching IPv4 address fails
        st.error("Failed to retrieve public IPv4 address.")


if __name__ == "__main__":
    main()  # Running the main function if the script is executed directly
