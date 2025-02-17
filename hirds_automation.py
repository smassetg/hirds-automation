from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

def log_message(message):
    with open("log.txt", "a", encoding="utf-8") as log_file:  # Force UTF-8 encoding
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_file.write(f"{timestamp} {message}\n")

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


def open_hirds(lat, lon):
    print("initialising chrome webdrive")

    # Setup Chrome WebDriver
    try:
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")  # Runs Chrome in the background (optional)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("chrome webdriver initialised successfully")

        # Open HIRDS website
        url = "https://hirds.niwa.co.nz/?_gl=1*1ijya2j*_ga*NDg4OTU2MDY2LjE3Mzk1OTc4MjY.*_ga_4CXN46915J*MTczOTc5Njk4Ny4zLjAuMTczOTc5Njk4Ny4wLjAuMA.."
        driver.get(url)
        print("Chrome should be opening now")
        time.sleep(3)  # Wait for page to load

        # Find the latitude input field and enter value
        print("Find lat field")
        lat_input = driver.find_element(By.NAME, "latitude")  # Adjust if needed
        lat_input.clear()
        lat_input.send_keys(str(lat))

        # Find the longitude input field and enter value
        print("Find long field")
        lon_input = driver.find_element(By.NAME, "longitude")  # Adjust if needed
        lon_input.clear()
        lon_input.send_keys(str(lon))

        print("entered lat long field successfully")

        # Select the "Depth-Duration" radio button
        print("Selecting Depth-Duration option...")
        depth_radio = driver.find_element(By.ID, "optionsRadios1")  # Using ID for accuracy
        depth_radio.click()
        print("Depth-Duration selected!")

        # Click the "Generate Report" button
        print("Clicking 'Generate Report' button...")
        generate_report_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
        generate_report_button.click()
        print("Report generation started!")

        # Wait for report to process
        time.sleep(5)  # Adjust based on how long the report takes to generate

        # Wait for the download button to appear
        print("Waiting for download button...")
        time.sleep(3)  # Adjust timing if needed

        # Click the "Download Excel" button
        print("Clicking 'Download Excel' button...")
        download_button = driver.find_element(By.CLASS_NAME, "glyphicon-download-alt")
        download_button.click()
        print("Download started!")

        # Wait for the file to download
        time.sleep(5)

        time.sleep(5)  # Wait for interactions to complete
        driver.quit()  # Close browser

        print("browser closed")

    except Exception as e:
        print(f"ERROR: {e}")

# Test with an example address
if __name__ == "__main__":
    address = "216 Clifford Street, Whataupoko, Gisborne, New Zealand"  # Change this
    lat, lon = get_lat_long(address)
    if lat and lon:
        print(f"Latitude: {lat}, Longitude: {lon}") #Debug print
        open_hirds(lat, lon) # Call the function
        log_message(f"SUCCESS: {address} → {lat}, {lon}")
    else:
        print("Failed to get coordinates.")
        log_message(f"ERROR: Failed to get coordinates for {address}")
