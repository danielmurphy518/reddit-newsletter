import time
import random
import os 
import csv
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description="Reddit Newsletter Scraper")
    parser.add_argument("--subreddit", type=str, default="triplej", help="Subreddit to scrape")
    return parser.parse_args()

def main():
    args = get_args()
    
    logger.info("Firing up Selenium...")
    options = Options()
    
    # This creates a folder in your project to save your login session
    script_dir = os.path.dirname(os.path.abspath(__file__))
    user_data_path = os.path.join(script_dir, "selenium_profile")
    options.add_argument(f"--user-data-dir={user_data_path}")
    
    driver = webdriver.Chrome(options=options)
    
    new_subreddit = args.subreddit
    subreddit_url = f"https://www.reddit.com/r/{new_subreddit}/new/"
    logger.info(f"Navigating to {subreddit_url}...")
    driver.get(subreddit_url)
    
    # Scraping logic for the last 24 hours
    logger.info(f"Scraping posts from the last 24 hours in r/{new_subreddit}...")
    posts_data = {}
    processed_ids = set()
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
    stop_scraping = False
    
    # Scroll and collect posts
    while not stop_scraping:
        # Reddit's modern UI uses 'shreddit-post' elements
        posts = driver.find_elements(By.TAG_NAME, "shreddit-post")
        
        if not posts:
            break
            
        for post in posts:
            post_id = post.get_attribute("id")
            if not post_id or post_id in processed_ids:
                continue
                
            permalink = post.get_attribute('permalink')
            if not permalink:
                continue

            post_url = f"https://www.reddit.com{permalink}"
            
            # Open post in a new tab
            driver.execute_script("window.open(arguments[0], '_blank');", post_url)
            driver.switch_to.window(driver.window_handles[1])
            
            try:
                # Wait for the <time> element to appear
                time_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "time"))
                )
                created_at = time_element.get_attribute("datetime")
                
                if created_at:
                    post_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    
                    if post_time < cutoff_time:
                        logger.info(f"Reached a post older than 24 hours ({post_time}). Stopping.")
                        stop_scraping = True
                        break
                    
                    # Scrape comments using the provided slot selector
                    comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div[slot="comment"]')
                    # Extract text and filter out empty strings
                    comments = [c.text.replace('\n', ' ').strip() for c in comment_elements if c.text.strip()]
                    
                    # Get title from the shreddit-post container in the detail view
                    detail_post = driver.find_element(By.TAG_NAME, "shreddit-post")
                    posts_data[post_id] = {
                        "title": detail_post.get_attribute("post-title"),
                        "link": post_url,
                        "timestamp": created_at,
                        "comments": comments
                    }
                    logger.info(f"Scraped: {posts_data[post_id]['title']}")
            except Exception as e:
                logger.warning(f"Failed to scrape details for {post_url}: {e}")
            finally:
                # Close tab and return to the main list
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            
            processed_ids.add(post_id)
            time.sleep(random.uniform(1, 2)) # Small delay between tabs

        if stop_scraping:
            break

        # Scroll down to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) # Brief pause to allow content to load

    # Export to CSV
    if posts_data:
        csv_file = "scraped_reddit_posts.csv"
        logger.info(f"Writing results to {csv_file}...")
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Post ID', 'Title', 'Link', 'Timestamp', 'Comments'])
            for pid, data in posts_data.items():
                # Join comments with a unique separator for CSV clarity
                comments_str = " | ".join(data['comments'])
                writer.writerow([pid, data['title'], data['link'], data['timestamp'], comments_str])
        logger.info("CSV export complete.")

    logger.info(f"Successfully scraped {len(posts_data)} posts.")
    for pid, data in posts_data.items():
        logger.info(f"Found: {data['title']} - {data['link']}")

    logger.info("Scraping complete. Closing browser.")
    driver.quit()

if __name__ == "__main__":
    main()
