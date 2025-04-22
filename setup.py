from binance.client import Client

from config import API_KEY, SECRET_KEY
from db.create_tables import create_tables
from db.db_handler import save_pair
from utils.logger import get_logger
from utils.trading import get_pairs

client = Client(API_KEY, SECRET_KEY)

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting setup...")
    logger.info("Creating tables...")
    create_tables()

    logger.info("Getting pairs...")
    current_pairs = get_pairs()
    logger.info(f"Found {len(current_pairs)} pairs")
    logger.info("Saving pairs...")
    for pair in current_pairs:
        try:
            base_asset = pair.get("base_asset")
            quote_asset = pair.get("quote_asset")
            symbol = pair.get("symbol")
            if not base_asset or not quote_asset or not symbol:
                logger.error(f"Missing base_asset, quote_asset, or symbol for pair {pair}")
                continue
            save_pair(symbol, base_asset, quote_asset)
        except Exception as e:
            logger.error(f"Error saving pair {pair['symbol']}: {e}")

    logger.info("Setup complete.")
