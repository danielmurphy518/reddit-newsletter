import time
import random
import os 
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")


#set subreddit to scrape
SUBREDDIT = 'askreddit'

def main():
    print("Firing up Selenium...")
    options = Options()
    # options.add_argument('--headless') # Uncomment this if you want the browser to run invisibly in the background
    driver = webdriver.Chrome(options=options)
    
    print(f"Navigating to r/{SUBREDDIT}...")
    driver.get(f"https://www.reddit.com/r/{SUBREDDIT}")
    
    print("Waiting for the login button to load...")
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        )
        login_button.click()
        print("Successfully clicked the login button!")
        
        print("Waiting for the username field to load...")
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-username"))
        )
        username_field.send_keys(username)
        print("Successfully entered the username!")
        
        print("Waiting for the password field to load...")
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-password"))
        )
        password_field.send_keys(password)
        print("Successfully entered the password!")
        
        print("Clicking the final Log In button...")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.login"))
        )
        submit_button.click()
        print("Successfully submitted the login form!")
        
    except Exception as e:
        print(f"An error occurred during the login process: {e}")
    
    # Adding a brief pause so you can visually confirm it worked before the script terminates
    time.sleep(99)
    #driver.quit()

if __name__ == "__main__":
    main()
