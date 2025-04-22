from typing import Any, Dict, List

from binance.client import Client

from config import API_KEY, PAIR_QUOTE, SECRET_KEY
from utils.filter_pairs import get_pairs_by_quote
from utils.logger import get_logger

logger = get_logger(__name__)
client = Client(API_KEY, SECRET_KEY)


def get_pairs() -> List[Dict[str, Any]]:
    """
    Retrieve all trading pairs available from the Binance exchange.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a trading pair.
        Each dictionary may include keys such as:

        - symbol (str): The trading symbol (e.g., 'ETHBTC').
        - status (str): Trading status (e.g., 'TRADING').
        - baseAsset (str): The base asset.
        - baseAssetPrecision (int): Precision of the base asset.
        - quoteAsset (str): The quote asset.
        - quotePrecision (int): Precision of the quote asset.
        - orderTypes (List[str]): Supported order types (e.g., 'LIMIT', 'MARKET').
        - icebergAllowed (bool): Whether iceberg orders are allowed.
        - isSpotTradingAllowed (bool): Whether spot trading is allowed for the pair.
        - filters (List[Dict[str, Any]]): List of trading rules (e.g., LOT_SIZE, PRICE_FILTER).
    
    Example:
    .. code-block:: python:
        [{
            "symbol": "ETHBTC",
            "status": "TRADING",
            "baseAsset": "ETH",
            "baseAssetPrecision": 8,
            "quoteAsset": "BTC",
            "quotePrecision": 8,
            "orderTypes": ["LIMIT", "MARKET"],
            "icebergAllowed": False,
            "isSpotTradingAllowed": True,
            "filters": [
                {
                    "filterType": "PRICE_FILTER",
                    "minPrice": "0.00000100",
                    "maxPrice": "100000.00000000",
                    "tickSize": "0.00000100"
                },
                {
                    "filterType": "LOT_SIZE",
                    "minQty": "0.00100000",
                    "maxQty": "100000.00000000",
                    "stepSize": "0.00100000"
                },
                {
                    "filterType": "MIN_NOTIONAL",
                    "minNotional": "0.00100000"
                }
            ]
        },
        ...
    ]
    """
    try:
        if not PAIR_QUOTE:
            raise ValueError("PAIR_QUOTE is not set")
        
        symbols = client.get_exchange_info().get('symbols', [])
        return get_pairs_by_quote(symbols, PAIR_QUOTE)
    except Exception:
        logger.error("Error getting pairs", exc_info=True)
        return []


def calculate_quantity(price: float, amount: float, step_size: float) -> float:
    """
    Calculate the quantity of a trade based on the price and amount.

    Args:
        price (float): The price of the asset.
        amount (float): The amount of money to spend on the trade.
    """
    raw_qty = amount / price
    return round(raw_qty - (raw_qty % step_size), 8)


def get_step_size(symbol_info: Dict[str, Any]) -> float:
    """
    Get the step size for a symbol.

    Args:
        symbol_info (Dict[str, Any]): The symbol information.
    """
    lot_size_filter = next(
        filter(lambda x: x["filterType"] == "LOT_SIZE", symbol_info["filters"])
    )
    return float(lot_size_filter["stepSize"])


def get_min_notional(symbol_info: Dict[str, Any]) -> float:
    """
    Get the minimum notional value for a symbol.

    Args:
        symbol_info (Dict[str, Any]): The symbol information.
    """
    for f in symbol_info.get("filters", []):
        if f.get("filterType") != "NOTIONAL":
            continue
        return float(f.get("minNotional", 0.0))
    return 0.0