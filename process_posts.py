import os
import csv
import logging
from openai import OpenAI
import argparse
from datetime import datetime
from dotenv import load_dotenv
import openai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser(description="Process Reddit posts with LLM")
    parser.add_argument("--subreddit", type=str, default="triplej", help="Subreddit to process")
    return parser.parse_args()

def load_posts_from_csv(filepath):
    """Reads the scraped CSV and formats it for the LLM."""
    if not os.path.exists(filepath):
        logger.error(f"File {filepath} not found.")
        return None

    formatted_content = ""
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            formatted_content += f"\n--- Post {i+1} ---\n"
            formatted_content += f"Title: {row['Title']}\n"
            formatted_content += f"Comments: {row['Comments']}\n"
    
    return formatted_content

def main():
    args = get_args()
    subreddit = args.subreddit

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        logger.error("OPENAI_API_KEY not found in .env file.")
        return

    client = OpenAI(api_key=api_key)
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.join("output", subreddit, current_date)
    csv_path = os.path.join(output_dir, "scraped_reddit_posts.csv")

    logger.info("Loading data from CSV...")
    content = load_posts_from_csv(csv_path)
    
    if not content:
        return

    is_monday = datetime.now().weekday() == 0
    time_period = "over the weekend (last 3 days)" if is_monday else "the last 24 hours"

    prompt = f"""
    You are a professional newsletter editor. Below is a list of Reddit posts and their top comments from {time_period}.
    For each individual post, provide a concise summary of its content and a synthesis of the key points being discussed in the comments.
    Please format the response clearly so that the information is presented per post.

    At the end of the newsletter, please add a brief summary section titled "Mentioned Artists" that lists the names of all the musical artists or bands mentioned in these posts and comments.

    Data:
    {content}
    """

    logger.info("Sending data to OpenAI...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        print("\n--- AI Newsletter Summary ---\n")
        print(response.choices[0].message.content)

        # Save the summary to a text file
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "newsletter_summary.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.choices[0].message.content)
        logger.info(f"Summary successfully saved to {output_path}")

    except openai.RateLimitError as e:
        logger.error(f"Quota or Rate Limit reached: {e}")
        print("\n[!] Error: You have likely run out of OpenAI credits or are using an invalid model name.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()