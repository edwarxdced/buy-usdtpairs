from binance.client import Client 
import time
from db_handler import save_pair, save_order, get_saved_pairs
from telegram import send_telegram_message

API_KEY = 'jD6shuP7R9oxoBOfUorit1ULFsctNjjn4572yuoqbgQ2RgTagL8sVJ8pUgp5ZvCQ'
SECRET_KEY = 'ZUFMX7ULpCBW40fh8t4TiD0grTjr9f1C4dJDfKPkrJtUfUfex3NXSsQBMUzJ5Hz2'

# Binance configuration
client = Client(API_KEY, SECRET_KEY)
AMOUNT_BUY = 20

def get_usdt_pairs():
    try:
        # Get information for all symbols
        exchange_info = client.get_exchange_info()
        symbols = exchange_info['symbols']
        
        # Filter only USDT pairs
        usdt_pairs = [
            symbol for symbol in symbols
            if symbol['quoteAsset'] == 'USDT' and symbol['status'] == 'TRADING' and symbol['isSpotTradingAllowed']
        ]
        
        return usdt_pairs
        
    except Exception as e:
        print(f"Error getting pairs: {e}")
        return []
    
def check_and_buy_new_pairs():
    try:
        # Get current and saved pairs
        current_pairs = get_usdt_pairs()
        saved_pairs = get_saved_pairs()
        # Print current and new pairs count
        
        new_pairs = [pair for pair in current_pairs if pair['symbol'] not in saved_pairs]
        print(f"Current pairs: {len(current_pairs)}, Saved pairs: {len(saved_pairs)}, New pairs: {len(new_pairs)}")
        
        for pair in new_pairs:
            try:
                symbol = pair['symbol']
                print(f"New pair found: {symbol}")
                
                # Get current price
                ticker = client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                
                # Calculate quantity to buy (20 USDT worth)
                quantity = AMOUNT_BUY / price
                
                # Round quantity according to Binance rules
                info = client.get_symbol_info(symbol)
                lot_size_filter = next(filter(lambda x: x['filterType'] == 'LOT_SIZE', info['filters']))
                step_size = float(lot_size_filter['stepSize'])
                quantity = round(quantity - (quantity % step_size), 8)
                
                # Execute buy order
                
                order = client.create_order(
                    symbol=symbol,
                    side='BUY',
                    type='MARKET',
                    quantity=quantity
                )
                # Save order to database
                save_order(symbol, quantity, price, AMOUNT_BUY, order)
                
                # Save new pair to usdt_pairs table
                save_pair(symbol, pair['baseAsset'], pair['quoteAsset'])
                
                print(f"Buy order executed for {symbol}: {quantity} at price {price}")
                # Send Telegram message with purchase details
                message = f"💰 New purchase made:\n\n" \
                         f"Symbol: {symbol}\n" \
                         f"Quantity: {quantity}\n" \
                         f"Price: {price} USDT\n" \
                         f"Total: {AMOUNT_BUY} USDT"
                send_telegram_message(message)
            except Exception as e:
                print(f"Error processing pair {symbol}: {e}")
                
        print("Check and buy new pairs process finished")
    except Exception as e:
        print(f"Error in check_and_buy_new_pairs: {e}")


if __name__ == "__main__":
    check_and_buy_new_pairs()
