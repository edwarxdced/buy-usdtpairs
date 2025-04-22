import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

AMOUNT_BUY: float = float(os.getenv("PAIR_AMOUNT", 20))
PAIR_QUOTE: Optional[str] = os.getenv("PAIR_QUOTE", "USDT")
API_KEY: Optional[str] = os.getenv("API_KEY")
SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
DB_HOST: Optional[str] = os.getenv("DB_HOST")
DB_USER: Optional[str] = os.getenv("DB_USER")
DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD")
DB_NAME: Optional[str] = os.getenv("DB_NAME")
TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

if API_KEY is None or SECRET_KEY is None or DB_HOST is None or DB_USER is None or DB_PASSWORD is None or DB_NAME is None:
    raise ValueError("API_KEY and SECRET_KEY and DB_HOST and DB_USER and DB_PASSWORD and DB_NAME must be set")