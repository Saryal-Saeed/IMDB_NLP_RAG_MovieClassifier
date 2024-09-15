import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,asc")

# Set implicit wait for dynamic content loading
driver.implicitly_wait(5)

# Function to scroll down slowly and check for the "100 more" button by text
def scroll_and_check_button_by_text():
    scroll_pause_time = 2  # Time to wait after each scroll (seconds)
    
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
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(1)  # Give some time for the button to be visible

        # Attempt to click the button using JavaScript
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(3)  # Wait for more content to load
    except Exception as e:
        print("Failed to click the '100 more' button:", e)

# Function to extract movie details from the page
def extract_movie_details():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    movies = []
    for movie_div in soup.find_all('li', class_='ipc-metadata-list-summary-item'):
        title = movie_div.find('h3', class_='ipc-title__text').text if movie_div.find('h3', class_='ipc-title__text') else 'N/A'
        year = movie_div.find('span', class_='sc-b189961a-8 hCbzGp dli-title-metadata-item').text if movie_div.find('span', class_='sc-b189961a-8 hCbzGp dli-title-metadata-item') else 'N/A'
        rating = movie_div.find('span', class_='ipc-rating-star--rating').text if movie_div.find('span', class_='ipc-rating-star--rating') else 'N/A'
        description = movie_div.find('div', class_='ipc-html-content-inner-div').text if movie_div.find('div', class_='ipc-html-content-inner-div') else 'N/A'
        
        movies.append({
            'Title': title,
            'Year': year, 
            'Rating': rating,
            'Description': description
        })
    print("content extracted", movie_div)
    return movies

# Main loop to load all content and extract data
all_movies = []

while True:
    try:
        load_more_button = scroll_and_check_button_by_text()  # Scroll slowly until the button appears
        load_more_content(load_more_button)  # Click the "100 more" button
        movies = extract_movie_details()  # Extract movie details from the loaded content
        all_movies.extend(movies)  # Append extracted data to the list
    except Exception as e:
        print("No more content to load or encountered an issue:", e)
        break

# Save the data to a CSV file
df = pd.DataFrame(all_movies)
df.to_csv('movies.csv', index=False)
print("Data has been extracted and saved to movies.csv")

time.sleep(5)  # Let the user observe results before closing
driver.quit()

