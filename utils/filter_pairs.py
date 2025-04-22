from typing import Any, Dict, List

from enums.symbol_status import SymbolStatus


def get_pairs_by_quote(symbols: List[Dict[str, Any]], quote_asset: str) -> List[Dict[str, Any]]:
    """
    Filter symbol list to get those trading in spot with a specific quote asset.
    
    Args:
        symbols (List[Dict]): List of symbol dictionaries from Binance exchange info.
        quote_asset (str): The quote asset to filter by (e.g., 'USDT').

    Returns:
        List[Dict[str, Any]]: Filtered list of symbols matching the criteria.
        Each symbol dictionary contains the following keys:
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
    return [
        symbol for symbol in symbols
        if symbol['quoteAsset'] == quote_asset and
        symbol['status'] == SymbolStatus.TRADING.value and
        symbol.get('isSpotTradingAllowed', False)
    ]