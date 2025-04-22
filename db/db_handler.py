from typing import Any, Dict, List

from db.connection import get_connection
from utils.logger import get_logger

logger = get_logger(__name__)


def get_saved_pairs() -> List[str]:
    """
    Get all saved pairs from the usdt_pairs table.

    Returns:
        List[str]: A list of symbols from the usdt_pairs table.
    
    Example:
    .. code-block:: python:
        ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    """
    query = "SELECT symbol FROM usdt_pairs"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return [str(row[0]) for row in results]


def save_pair(symbol: str, base_asset: str, quote_asset: str) -> None:
    """
    Save a pair to the usdt_pairs table.

    Args:
        symbol (str): The symbol of the pair.
        base_asset (str): The base asset of the pair.
        quote_asset (str): The quote asset of the pair.
    """
    query = """
    INSERT IGNORE INTO usdt_pairs (symbol, base_asset, quote_asset)
    VALUES (%s, %s, %s)
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (symbol, base_asset, quote_asset))
            conn.commit()
    except Exception as e:
        logger.error(f"Error saving pair: {e}", exc_info=True)


def save_order(symbol: str, quantity: float, price: float, usdt_amount: float, response: Dict[str, Any]) -> None:
    """
    Save an order to the orders table.

    Args:
        symbol (str): The symbol of the pair.
        quantity (float): The quantity of the order.
        price (float): The price of the order.
        usdt_amount (float): The amount of USDT used in the order.
        response (Dict[str, Any]): The response from the order.
    """
    query = """
    INSERT INTO orders (symbol, quantity, price, usdt_amount, response)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (symbol, quantity, price, usdt_amount, str(response)))
            conn.commit()
    except Exception as e:
        logger.error(f"Error saving order: {e}", exc_info=True)
