from binance.client import Client 
from db_handler import create_table, create_orders_table, save_pair



def save_all_pairs_usdt():
    client = Client()
    try:
        
        exchange_info = client.get_exchange_info()
        symbols = exchange_info['symbols']
        
        # Filter only USDT pairs
        usdt_pairs = [
            symbol for symbol in symbols
            if symbol['quoteAsset'] == 'USDT' and symbol['status'] == 'TRADING' and symbol['isSpotTradingAllowed']
        ]
        
        for pair in usdt_pairs:
            symbol = pair['symbol']
            base_asset = pair['baseAsset']
            quote_asset = pair['quoteAsset']
            try:
                save_pair(symbol, base_asset, quote_asset)
            except Exception as e:
              print(f'An exception occurred: {e}')
        
    except Exception as e:
        print(f"Error saving prices: {e}")
        
        
if __name__ == "__main__":
    create_table()
    create_orders_table()
    save_all_pairs_usdt()