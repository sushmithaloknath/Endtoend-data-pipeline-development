from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
import csv

# Define search keyword
search_query = "laptops"

# Set up WebDriver path
script_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(script_dir, "chromedriver.exe")

# Initialize WebDriver with improved settings
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
options.add_argument("--incognito")  # Open in incognito mode
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")  # Fake user-agent

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open Amazon
driver.get("https://www.amazon.in")

# Wait for the search box to appear
try:
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
except Exception as e:
    print("❌ Error: Couldn't find search box!", e)

# Random delay to avoid detection
time.sleep(random.uniform(5, 8))

# Check if CAPTCHA is triggered
if "Enter the characters" in driver.page_source:
    input("⚠️ CAPTCHA detected! Solve it manually, then press Enter to continue...")

# CSV file setup
csv_filename = os.path.join(script_dir, "amazon_products.csv")
product_list = [["Product Name", "Price", "Rating", "Reviews"]]

# Number of pages to scrape
max_pages = 5  # Change this to scrape more pages

# Function to scroll slowly and visibly
def scroll_slowly(driver, scroll_pause_time=1, scroll_increment=300):
    last_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll = 0
    while current_scroll < last_height:
        # Scroll down by a small increment
        driver.execute_script(f"window.scrollTo(0, {current_scroll});")
        current_scroll += scroll_increment
        print(f"🔄 Scrolled to {current_scroll}px")
        time.sleep(scroll_pause_time)  # Wait for the page to load

        # Update the last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height > last_height:
            last_height = new_height

# Function to highlight the "Next" button
def highlight_next_button(driver):
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")
        driver.execute_script("arguments[0].style.border='3px solid red';", next_button)  # Highlight with a red border
        print("🔴 Highlighted the 'Next' button.")
        time.sleep(2)  # Pause to see the highlight
    except Exception as e:
        print(f"⚠️ Error highlighting 'Next' button: {e}")

# Loop through pages
for page in range(1, max_pages + 1):
    print(f"\n📄 Scraping Page {page}...\n")

    # Scroll slowly to load all products
    scroll_slowly(driver)

    # Extract product details
    products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    for product in products:
        try:
            name = product.find_element(By.TAG_NAME, "h2").text
        except:
            name = "N/A"

        try:
            price = product.find_element(By.CLASS_NAME, "a-price-whole").text
        except:
            price = "N/A"

        try:
            rating_element = product.find_element(By.XPATH, ".//span[contains(@class, 'a-icon-alt')]")
            rating = rating_element.get_attribute("innerHTML").split()[0]
        except:
            rating = "N/A"

        try:
            reviews = product.find_element(By.XPATH, ".//span[contains(@class, 'a-size-base s-underline-text')]").text
        except:
            reviews = "N/A"

        # Debugging: Print extracted details
        print(f"📌 Product: {name}\n   ➡ Price: ₹{price}\n   ⭐ Rating: {rating}\n   📝 Reviews: {reviews}\n")

        # Append data to list
        product_list.append([name, f"₹{price}", rating, reviews])

    # Highlight and click the "Next" button
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")
        if "s-pagination-disabled" in next_button.get_attribute("class"):
            print("✅ Reached the last page.")
            break  # Stop if the "Next" button is disabled

        # Highlight the "Next" button
        highlight_next_button(driver)

        # Click the "Next" button using JavaScript
        driver.execute_script("arguments[0].click();", next_button)
        print("🖱️ Clicked the 'Next' button.")
        time.sleep(random.uniform(5, 10))  # Random delay before scraping the next page
    except Exception as e:
        print(f"⚠️ Error clicking 'Next' button: {e}")
        break

# Save data to CSV
with open(csv_filename, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerows(product_list)

print(f"\n✅ Data saved successfully in {csv_filename}!")

# Close the browser
driver.quit()