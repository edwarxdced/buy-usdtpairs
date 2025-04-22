import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import get_logger

logger = get_logger(__name__)


def send_telegram_message(message: str):
    """
    Sends a message to a Telegram chat or group using the Telegram Bot API.

    Parameters:
        message (str): The message to send.

    Returns:
        None
    """
    
    TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(TELEGRAM_URL, data=data)
        if response.status_code == 200:
            logger.info("Message sent successfully.")
        else:
            logger.error(f"Failed to send message: {response.status_code}")
            logger.error(response.json())
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    send_telegram_message("Hello! This is a test message from my Telegram bot.")
