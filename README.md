# reddit-newsletter
Selenium Scraper + LLM processing to develop subreddit activity summaries and insights

## Overview (WIP) 

This application is divided into three components
- Selenium Python Scraper
- LLM Processing
- SMTP email system

I aim to keep these components as separate as possible so they can be modified/adjusted/switched out as needed. At the moment I am using openAI/chatGPT for my LLM processing service

**Please be aware that data scraping violates Reddit's TOS: proceed with caution!! If you don't wish you face blocks/bans from Reddit I would reccomend running this with a VPN**


## Installation
1. **Clone the repository**
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install selenium python-dotenv
   ```
4. **Configuration:** Create a `.env` file with your `REDDIT_USERNAME` and `REDDIT_PASSWORD`.

**Safety Warning:** You will need a Reddit account for the scraper to work. Please be aware that Reddit has sophisticated ban evasion systems. Your computer/IP address can be banned from reddit. For 100% safety I would *highly* reccomend using a proxy and a brand new Reddit account when scraping.
