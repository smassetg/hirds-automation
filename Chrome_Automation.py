from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import datetime
import time

def log_message(message):
    with open(".venv/log.txt", "a", encoding="utf-8") as log_file:  # Force UTF-8 encoding
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


# Attach to existing Chrome session instead of opening a new one
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Connect to running Chrome

driver = webdriver.Chrome(options=options)
print("✅ Connected to existing Chrome window!")

# Now start your next automation step
print("Now starting next step...")

# Wait for the toolbar close button to appear
print("Closing toolbar for better view...")
close_toolbar_button = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@class='toolbar-action-button']/img[contains(@title, 'Close toolbar')]"))
)
close_toolbar_button.click()
print("✅ Toolbar closed successfully!")
time.sleep(2)  # Allow UI to update

# Automate the search bar entry
search_bar = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "gcx_search"))
)

# Enter address (truncated to work correctly)
print("Entering address into search bar...")
search_bar.clear()
search_bar.send_keys("216 Clifford Street")
time.sleep(1)  # Small delay to mimic human typing

# Find the search button
print("Clicking search button...")
search_button = WebDriverWait(driver, 3).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "search-button"))
)
search_button.click()

print("Search performed successfully!")

# Wait for the search result "Street Address" to appear
print("Waiting for search results...")
street_address_result = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//strong[contains(@class, 'gcx-list-label') and contains(., 'Street Address')]"))
)

# Click the first search result
print("Clicking on 'Street Address' search result...")
street_address_result.click()
time.sleep(2)  # Small delay to allow next list to load

# Wait for the specific address entry (216 CLIFFORD STREET) to appear
print("Waiting for the specific address result...")
address_result = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//strong[contains(@class, 'gcx-list-label')]//div[contains(@class, 'feature-label') and contains(text(), '216 CLIFFORD STREET')]"))
)

# Click on the specific address result
print("Clicking on '216 CLIFFORD STREET' search result...")
address_result.click()

print("✅ Address selected successfully!")
#
# # Wait for the highlight circle to appear
# print("Waiting for the highlight circle...")
# highlight_circle = WebDriverWait(driver, 5).until(
#     EC.presence_of_element_located((By.XPATH, "//g[@id='DefaultHighlightLayer_layer']//circle"))
# )
#
# print("✅ Highlight circle detected!")
#
# # Get circle position
# circle_x = int(highlight_circle.get_attribute("cx"))
# circle_y = int(highlight_circle.get_attribute("cy"))
# print(f"Circle found at ({circle_x}, {circle_y})")
#
#
# # Get map viewport element
# map_element = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "ol-viewport"))  # Adjust selector if needed
# )
#
# # Simulate dragging the map to center the highlight circle
# actions = ActionChains(driver)
# actions.click_and_hold(map_element).move_by_offset(-circle_x, -circle_y).release().perform()
#
# print("✅ Map centered on highlight circle!")
# time.sleep(2)  # Allow UI to update


# Wait for the scale dropdown to appear
print("Selecting 1:1000 scale...")
scale_dropdown = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "scale-selector-select"))
)

# Select the "1:1000" option
select = Select(scale_dropdown)
select.select_by_visible_text("1:1,000")

print("✅ Zoom set to 1:1000 successfully!")
time.sleep(2)  # Allow time for zooming effect

# #
# def open_hirds(lat, lon):
#     print("initialising chrome webdrive")
#
#     # Setup Chrome WebDriver
#     try:
#         options = webdriver.ChromeOptions()
#         #options.add_argument("--headless")  # Runs Chrome in the background (optional)
#         options.add_experimental_option("detach", True)
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         print("chrome webdriver initialised successfully")
#
#         # Open HIRDS website
#         url = "https://maps.gdc.govt.nz/H5V2_12/Index.html?viewer=TairawhitiServices"
#         driver.get(url)
#         print("Chrome should be opening now")
#         time.sleep(20)  # Wait for page to load
#
#         # Confirm disclaimer - click proceed button
#         print("Clicking 'proceed' button...")
#         proceed_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed')]")
#         proceed_button.click()
#         print("clicked proceed worked")
#
#         # There will need to be a script here to account for when the GIS viewer issues as error from mal-loaded layers (happens occassionally)
#
#
#         # # Find the latitude input field and enter value
#         # print("Find lat field")
#         # lat_input = driver.find_element(By.NAME, "latitude")  # Adjust if needed
#         # lat_input.clear()
#         # lat_input.send_keys(str(lat))
#         #
#         # # Find the longitude input field and enter value
#         # print("Find long field")
#         # lon_input = driver.find_element(By.NAME, "longitude")  # Adjust if needed
#         # lon_input.clear()
#         # lon_input.send_keys(str(lon))
#         #
#         # print("entered lat long field successfully")
#         #
#         # # Select the "Depth-Duration" radio button
#         # print("Selecting Depth-Duration option...")
#         # depth_radio = driver.find_element(By.ID, "optionsRadios1")  # Using ID for accuracy
#         # depth_radio.click()
#         # print("Depth-Duration selected!")
#         #
#         #
#         #
#         # # Wait for report to process
#         # time.sleep(5)  # Adjust based on how long the report takes to generate
#         #
#         # # Wait for the download button to appear
#         # print("Waiting for download button...")
#         # time.sleep(3)  # Adjust timing if needed
#         #
#         # # Click the "Download Excel" button
#         # print("Clicking 'Download Excel' button...")
#         # download_button = driver.find_element(By.CLASS_NAME, "glyphicon-download-alt")
#         # download_button.click()
#         # print("Download started!")
#         #
#         # # Wait for the file to download
#         # time.sleep(5)
#         #
#         # time.sleep(5)  # Wait for interactions to complete
#         # driver.quit()  # Close browser
#         #
#         # print("browser closed")
#
#     except Exception as e:
#         print(f"ERROR: {e}")
#
# # Test with an example address
# if __name__ == "__main__":
#     address = "216 Clifford Street, Whataupoko, Gisborne, New Zealand"  # Change this
#     address2 = "216 Cliffor Street"
#     lat, lon = get_lat_long(address)
#     if lat and lon:
#         print(f"Latitude: {lat}, Longitude: {lon}") #Debug print
#         open_hirds(lat, lon) # Call the function
#         log_message(f"SUCCESS: {address} → {lat}, {lon}")
#     else:
#         print("Failed to get coordinates.")
#         log_message(f"ERROR: Failed to get coordinates for {address}")
