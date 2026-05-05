#!/bin/bash

# Set the subreddit you want to scrape, default is "triplej" if not provided
SUBREDDIT=${1:-triplej}

echo "🚀 Starting Reddit Newsletter Pipeline for r/$SUBREDDIT..."

echo "==== STEP 1: Scraping Reddit ===="
python3 main.py --subreddit $SUBREDDIT

echo "==== STEP 2: Processing with LLM ===="
python3 process_posts.py

echo "==== STEP 3: Sending Email ===="
python3 send_newsletter.py

echo "✅ Pipeline complete!"
