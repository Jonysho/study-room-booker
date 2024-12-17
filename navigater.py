from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
LOGIN_URL = os.getenv("LOGIN_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# --- FUNCTION DEFINITIONS ---
def login_to_resource_booker(driver):
    """Log into the Resource Booker website."""
    try:
        driver.get(LOGIN_URL)
        print("Opened the Resource Booker website.")
        
        # Click the login button
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "ember533"))
        )
        login_button.click()
        # Wait for login page to load and input credentials
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))
        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        username_field.send_keys(USERNAME)
        time.sleep(1)
        password_field.send_keys(PASSWORD)
        time.sleep(1)

        # Submit the login form
        submit_button = driver.find_element(By.NAME, "_eventId_proceed")
        submit_button.click()

        # Wait for the post-login page to load
        time.sleep(5)  # Adjust for network speed
        print("Login successful!")
        locators = [
            (By.XPATH, "//a[contains(@class, 'sidebarNav-link') and contains(., 'Make a booking')]"),
            (By.XPATH, "//a[contains(@class, 'resourcesGrid-item-link') and contains(., 'Library Study Rooms')]"),
            (By.XPATH, "//a[contains(@class, 'resourcesList-item-link') and contains(., 'Learning Commons')]"),
        ]
        for locator in locators:
            # Wait for the element to be present
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(locator)
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll to the element if not visible
            element.click()
            time.sleep(2)  # Add delay to let the next page load

    except TimeoutException as e:
        print("Error: Login process timed out.", e)
        driver.quit()
        exit()

def find_availability(driver, room_name):
    """Find the availability of a study room."""
    # Click the day button to view the day's schedule
    button = (By.XPATH, "//button[contains(@class, 'chronos-headerView-button') and contains(@data-view-type, 'day')]")
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(button)
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll to the element if not visible
    element.click()

    time.sleep(4)
    # Wait for the hour grid and events to be present
    hour_grid = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".chronos-weekView-hourGrid"))
    )
    events = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".chronos-weekView-events"))
    )

    # Get all the hour grid items
    hour_grid_items = hour_grid.find_elements(By.CSS_SELECTOR, ".chronos-weekView-hourGrid-item")

    # Get all the event times
    event_times = events.find_elements(By.CSS_SELECTOR, ".chronos-weekView-event")

    # Extract the half-hour slots from the event times
    booked_slots = set()
    for event in event_times:
        from_time = event.get_attribute("data-from-time")
        to_time = event.get_attribute("data-to-time")
        from_hour, from_minute = map(int, from_time.split("T")[1].split(":")[:2])
        to_hour, to_minute = map(int, to_time.split("T")[1].split(":")[:2])
        start_slot = from_hour * 2 + (1 if from_minute >= 30 else 0)
        end_slot = to_hour * 2 + (1 if to_minute >= 30 else 0)
        booked_slots.update(range(start_slot, end_slot))

    # Find and format the available slots
    available_slots = []
    current_start = None
    for item in hour_grid_items:
        hour = int(item.get_attribute("data-hour"))
        for half_hour in [0, 30]:
            slot = hour * 2 + (1 if half_hour == 30 else 0)
            if slot not in booked_slots:
                if current_start is None:
                    current_start = slot
            else:
                if current_start is not None:
                    available_slots.append((current_start, slot))
                    current_start = None
    if current_start is not None:
        available_slots.append((current_start, current_start + 1))

    # Format the available slots
    formatted_slots = []
    for start, end in available_slots:
        start_hour = start // 2
        start_minute = "30" if start % 2 else "00"
        end_hour = end // 2
        end_minute = "30" if end % 2 else "00"
        formatted_slots.append(f"{start_hour}:{start_minute} - {end_hour}:{end_minute}")

    print(f"{room_name.split(" ")[2]}: {formatted_slots}")

def visit_study_rooms(driver):
    """Visit each study room, and click the back button."""
    room_names = [
        "AGLC Room 312 Group Study Space",
        "AGLC Room 311 Group Study Space",
        "AGLC Room 310 Group Study Space",
        "AGLC Room 309 Group Study Space",
        "AGLC Room 308 Group Study Space",
        "AGLC Room 307 Group Study Space",
        "AGLC Room 306 Group Study Space",
        "AGLC Room 305 Group Study Space",
        "AGLC Room 304 Group Study Space",
        "AGLC Room 303 Group Study Space",
        "AGLC Room 302 Group Study Space",
        "AGLC Room 301 Group Study Space",
        "AGLC Room 212 Group Study Space",
        "AGLC Room 211 Group Study Space",
        "AGLC Room 210 Group Study Space",
        "AGLC Room 209 Group Study Space",
        "AGLC Room 208 Group Study Space",
        "AGLC Room 207 Group Study Space",
        "AGLC Room 206 Group Study Space",
        "AGLC Room 205 Group Study Space",
        "AGLC Room 204 Group Study Space",
        "AGLC Room 203 Group Study Space",
        "AGLC Room 202 Group Study Space",
        "AGLC Room 201 Group Study Space",
        "AGLC Room 104 Group Study Space",
        "AGLC Room 103 Group Study Space",
        "AGLC Room 102 Group Study Space",
        "AGLC Room 101 Group Study Space"
        "AGLC Room -101 Group Study Space",
        "AGLC Room -102 Group Study Space",
    ]

    try:
        for room_name in room_names:
            button = (By.XPATH, "//button[contains(@class, 'button--primary') and contains(., 'Show more results')]")
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(button)
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll to the element if not visible
            element.click()

            # Wait for the list of study rooms to be present
            study_rooms_list = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".resourcesList-items"))
            )

            # Find the room link by its name
            room_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f".//a[contains(@class, 'resourcesList-item-link')]//span[contains(text(), '{room_name}')]"))
            )

            # Scroll to and click the room link
            driver.execute_script("arguments[0].scrollIntoView(true);", room_link)
            room_link.click()
            
            # Wait 2 seconds in the room
            find_availability(driver, room_name)

            # Click the 'back' button to return to the room list
            back_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.at-goBack"))
            )
            back_button.click()

    except TimeoutException as e:
        print("Error: Process timed out.", e)
        driver.quit()
        exit()
    except Exception as e:
        print("An error occurred:", e)
        driver.quit()
        exit()

# --- MAIN SCRIPT ---
if __name__ == "__main__":
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # Ensure ChromeDriver is in PATH
    
    try:
        # Step 1: Log into the website
        login_to_resource_booker(driver)

        # Step 2: Visit all study rooms
        visit_study_rooms(driver)

    finally:
        # Optional: Keep the browser open briefly before closing
        time.sleep(5)
        driver.quit()
        print("Closed the browser.")
