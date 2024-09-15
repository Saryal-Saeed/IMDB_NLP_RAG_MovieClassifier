from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is installed and in PATH
driver.get("https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,asc")

# Set implicit wait for dynamic content loading
driver.implicitly_wait(5)

# Function to scroll down slowly and check for the "100 more" text
def scroll_and_check_button_by_text():
    scroll_pause_time = 2  # Time to wait after each scroll (seconds)
    
    # Start scrolling incrementally
    while True:
        # Scroll down by window height
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(scroll_pause_time)  # Wait for a bit to let the page load
        
        try:
            # Check if an element with text '100 more' appears
            load_more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button'))
            )
            print("Found '100 more' button!")
            return load_more_button
        except Exception:
            pass  # If the button is not found, keep scrolling down

# Function to click the "100 more" button
def load_more_content(load_more_button):
    try:
        load_more_button.click()  # Click the button
        time.sleep(3)  # Wait for more content to load
    except Exception as e:
        print("Failed to click the '100 more' button:", e)

# Main loop to load all content
while True:
    try:
        load_more_button = scroll_and_check_button_by_text()  # Scroll slowly until the button appears
        load_more_content(load_more_button)  # Click the "100 more" button
    except Exception as e:
        print("No more content to load or encountered an issue:", e)
        break

# Optionally: You can save the page content or do further processing here

time.sleep(5)  # Let the user observe results before closing
driver.quit()
