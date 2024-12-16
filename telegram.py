import requests

def send_telegram_message(message: str):
    """
    Sends a message to a Telegram chat or group using the Telegram Bot API.

    Parameters:
        message (str): The message to send.

    Returns:
        None
    """
    # Your bot token and chat ID
    BOT_TOKEN = "6463915585:AAE7eBZUqrSBaZor1WSU94E5RUCsubyG1t0"
    CHAT_ID = "7084270896"

    # Telegram API URL
    TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Payload for the API request
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    # Send the request to Telegram
    try:
        response = requests.post(TELEGRAM_URL, data=data)
        if response.status_code == 200:
            print("Message sent successfully.")
        else:
            print(f"Failed to send message: {response.status_code}")
            print(response.json())  # Print error details
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    test_message = "Hello! This is a test message from my Telegram bot."
    send_telegram_message(test_message)
