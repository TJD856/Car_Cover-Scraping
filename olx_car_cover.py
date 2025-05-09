from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import os

# Url for the Olx search 
base_url = "https://www.olx.in/items/q-car-cover"

# Initialize variables
csv_file_path = os.path.abspath('olx_car_cover_results.csv')
driver = None

try:
    # Set up Selenium WebDriver with additional options
    options = Options()
    # options.add_argument('--headless')  # Commented out headless mode for debugging
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-webgl')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    options.add_argument('--window-size=1920,1080')

    service = Service('C:\\Windows\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    # Open the url
    print("Opening URL:", base_url)
    driver.get(base_url)
    time.sleep(5)  # Wait for initial page load
    
    # Save the page source for debugging
    with open("debug_olx.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("Saved page source to debug_olx.html")

    # Create CSV file first
    print(f"Creating CSV file at: {csv_file_path}")
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Location', 'URL', 'Description'])
        print("CSV header written")

    # Try to find any content on the page
    print("\nSearching for content on the page...")
    
    # Get all links on the page
    links = driver.find_elements(By.TAG_NAME, 'a')
    print(f"Found {len(links)} links on the page")

    # Get all text elements
    text_elements = driver.find_elements(By.XPATH, "//*[text()]")
    print(f"Found {len(text_elements)} text elements on the page")

    # Process the content
    items_processed = 0
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Process links
        for link in links:
            try:
                href = link.get_attribute('href')
                text = link.text.strip()
                if href and text and 'car-cover' in href.lower():
                    writer.writerow([text, 'N/A', 'N/A', href, 'Link found'])
                    items_processed += 1
                    print(f"Processed link: {text}")
            except Exception as e:
                print(f"Error processing link: {str(e)}")

        # Process text elements
        for element in text_elements:
            try:
                text = element.text.strip()
                if text and len(text) > 10 and 'car' in text.lower():
                    writer.writerow([text, 'N/A', 'N/A', 'N/A', 'Text content found'])
                    items_processed += 1
                    print(f"Processed text: {text[:50]}...")
            except Exception as e:
                print(f"Error processing text element: {str(e)}")

        print(f"\nTotal items processed: {items_processed}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Close the browser if it was created
    if driver:
        driver.quit()
    
    # Verify if file was created and has content
    if os.path.exists(csv_file_path):
        file_size = os.path.getsize(csv_file_path)
        print(f"\nScraping completed. Results saved in: {csv_file_path}")
        print(f"CSV file exists at: {csv_file_path}")
        print(f"File size: {file_size} bytes")
        
        if file_size > 0:
            print("CSV file has been created with content!")
        else:
            print("Warning: CSV file is empty!")
    else:
        print("\nWarning: CSV file was not created!")