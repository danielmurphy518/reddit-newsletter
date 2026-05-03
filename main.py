import time
import random
import os 
from dotenv import load_dotenv
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
#subreddit to scrape
SUBREDDIT = 'askreddit'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Firing up Selenium...")
    options = Options()
    driver = webdriver.Chrome(options=options)
    
    logger.info(f"Navigating to r/{SUBREDDIT}...")
    driver.get(f"https://www.reddit.com/r/{SUBREDDIT}")
    
    logger.info("Waiting for the login button to load...")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()
        logger.info("Successfully clicked the login button!")
        
        logger.info("Waiting for the username field to load...")
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-username"))
        )
        username_field.send_keys(username)
        logger.info("Successfully entered the username!")
        
        logger.info("Waiting for the password field to load...")
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-password"))
        )
        password_field.send_keys(password)
        logger.info("Successfully entered the password!")
        
        logger.info("Clicking the final Log In button...")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.login"))
        )
        submit_button.click()
        logger.info("Successfully submitted the login form!")
        
    except Exception as e:
        logger.error(f"An error occurred during the login process: {e}", exc_info=True)
    
    # Generate a random sleep duration between 1 and 67 seconds
    random_sleep_duration = random.randint(1, 67)
    logger.info(f"Sleeping for {random_sleep_duration} seconds before navigating to the next subreddit...")
    time.sleep(random_sleep_duration)
    
    new_subreddit = 'triplej'
    logger.info(f"Navigating to r/{new_subreddit}...")
    driver.get(f"https://www.reddit.com/r/{new_subreddit}")
    
    time.sleep(99) # Keep this for now to observe the new page
    #driver.quit()

if __name__ == "__main__":
    main()
