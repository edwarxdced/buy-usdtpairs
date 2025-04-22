from typing import Any, Dict

from binance.client import Client

from config import AMOUNT_BUY, API_KEY, SECRET_KEY
from db.db_handler import get_saved_pairs, save_order, save_pair
from enums.order import OrderSide, OrderType
from utils.logger import get_logger
from utils.telegram import send_telegram_message
from utils.trading import (calculate_quantity, get_min_notional, get_pairs,
                           get_step_size)

client = Client(API_KEY, SECRET_KEY)

logger = get_logger(__name__)
logger.info("Bot started.")


def process_pair(pair: Dict[str, Any]) -> None:
    """
    Process a new trading pair.

    Args:
        pair (Dict[str, Any]): The pair to process.
    """
    symbol = pair.get("symbol")
    base_asset = pair.get("baseAsset")
    quote_asset = pair.get("quoteAsset")
    if not symbol or not base_asset or not quote_asset:
        logger.error("Symbol, baseAsset, or quoteAsset is None")
        return
    
    logger.info(f"Processing new pair: {symbol}")
    ticker = client.get_symbol_ticker(symbol=symbol)
    price = float(ticker.get("price"))

    #symbol_info = client.get_symbol_info(symbol)
    step_size = get_step_size(pair)
    quantity = calculate_quantity(price, AMOUNT_BUY, step_size)
    min_notional = get_min_notional(pair)
    if quantity < min_notional:
        logger.info(f"Quantity is less than min notional for {symbol}")
        return

    try:
        order = client.create_order(
            symbol=symbol,
            side=OrderSide.BUY.value,
            type=OrderType.MARKET.value,
            quantity=quantity
        )
        
        save_order(symbol, quantity, price, AMOUNT_BUY, order)
        save_pair(symbol, base_asset, quote_asset)

        send_telegram_message(
            f"💰 New purchase made:\n"
            f"Symbol: {symbol}\nQuantity: {quantity}\n"
            f"Price: {price} USDT\nTotal: {AMOUNT_BUY} USDT"
        )
    except Exception as e:
        logger.error(f"Error creating order for {symbol}: {e}", exc_info=True)
        send_telegram_message(f"Error creating order for {symbol}: {e}")


def process_new_pairs():
    try:
        current_pairs = get_pairs()
        saved_symbols = get_saved_pairs()
        new_pairs = [p for p in current_pairs if p["symbol"] not in saved_symbols]

        logger.info(f"Found {len(new_pairs)} new pairs.")

        for pair in new_pairs:
            symbol = pair["symbol"]
            try:
                process_pair(pair)
            except Exception:
                logger.error(f"Error processing {symbol}", exc_info=True)
                
    except Exception:
        logger.critical("Error in process_new_pairs", exc_info=True)


if __name__ == "__main__":
    send_telegram_message("Checking for new trading pairs and buying opportunities...")
    process_new_pairs()
