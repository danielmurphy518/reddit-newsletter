import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def send_email(html_content, subject="Daily Reddit Newsletter"):
    """Sends the formatted HTML content via email using SMTP."""
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not all([sender, password, receiver]):
        logger.error("Email configuration missing in .env (EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER).")
        return

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))

    try:
        logger.info(f"Connecting to {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade to a secure connection
            server.login(sender, password)
            server.send_message(msg)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def main():
    load_dotenv()
    
    # Path to the generated newsletter summary
    file_path = "/Users/danielmurphy/Documents/Portfolio/reddit-newsletter/newsletter_summary.txt"
    
    if not os.path.exists(file_path):
        logger.error(f"Newsletter file not found at: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    send_email(html_content)

if __name__ == "__main__":
    main()
