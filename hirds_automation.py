from geopy.geocoders import Nominatim
import time

def get_lat_long(address):
    geolocator = Nominatim(user_agent="hirds_automation")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Test with an example address
if __name__ == "__main__":
    address = "186 Fox Street, Whataupoko, Gisborne, New Zealand"  # Change this
    lat, lon = get_lat_long(address)
    if lat and lon:
        print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("Failed to get coordinates.")
