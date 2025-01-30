from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Add this import
from PIL import Image
import pytesseract
import time
import os

# Configure the path to tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def scrape_website_with_ocr(url):
    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    # Initialize the driver with Service object
    service = Service(executable_path='./chromedriver-win64/chromedriver.exe')  # Path to your chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(3)
        driver.save_screenshot('./images/screenshot.png')
        image = Image.open('./images/screenshot.png')
        text = pytesseract.image_to_string(image)

        # Delete screenshot after processing
        os.remove('./images/screenshot.png')

        return text
    finally:
        driver.quit()

# Usage
website_text = scrape_website_with_ocr('https://gmgn.ai/new-pair?chain=sol')
print(website_text)