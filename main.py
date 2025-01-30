import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract
import time
import os

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def scrape_website_with_ocr(url):
    os.makedirs('./images', exist_ok=True)
    
    # Use undetected_chromedriver's native options
    options = uc.ChromeOptions()
    
    # Simplified configuration for undetected_chromedriver
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Headless mode configuration
    options.add_argument('--headless=new')
    
    # User agent configuration
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')

    try:
        # Initialize undetected_chromedriver with auto-version matching
        driver = uc.Chrome(
            options=options,
            version_main=120,  # Match your Chrome version
            driver_executable_path='./chromedriver-win64/chromedriver.exe'
        )
        
        # Stealth configuration
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Navigation with proper waiting
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        # Screenshot and OCR
        screenshot_path = './images/screenshot.png'
        driver.save_screenshot(screenshot_path)
        text = pytesseract.image_to_string(Image.open(screenshot_path))
        os.remove(screenshot_path)
        
        return text
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
        return None
        
    finally:
        if 'driver' in locals():
            try:
                driver.quit()
            except:
                pass

# Usage
website_text = scrape_website_with_ocr('https://gmgn.ai/new-pair?chain=sol')
print(website_text)