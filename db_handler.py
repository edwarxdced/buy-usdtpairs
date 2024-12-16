from typing import List, Union, Dict, Any
from decimal import Decimal
from datetime import datetime, date, time, timedelta
import mysql.connector
import json

DbData = Union[Decimal, bytes, date, datetime, float, int, str, time, timedelta, None]
DbConfig = Dict[str, str]

db_config: DbConfig = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'binance_pairs'
}



def get_saved_pairs()->List[str]:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT symbol FROM usdt_pairs")
        rows = cursor.fetchall()
        pairs = [str(row[0]) for row in rows if isinstance(row, tuple) and len(row) > 0 and isinstance(row[0], (str, int))]
        
        return pairs
        
    except Exception as e:
        print(f"Error getting saved pairs: {e}")
        return []
        
    finally:
        if conn.is_connected():
            cursor.close() 
            conn.close()

def create_orders_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                symbol TEXT,
                quantity FLOAT,
                price FLOAT, 
                total_usdt FLOAT,
                order_response JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("orders table created successfully")
        conn.commit()
        
    except Exception as e:
        print(f"Error creating orders table: {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def save_order(symbol: str, quantity: float, price:float, total_usdt:float, order_response: Dict) -> None:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO orders (symbol, quantity, price, total_usdt, order_response)
            VALUES (%s, %s, %s, %s, %s)
        """, (symbol, quantity, price, total_usdt, json.dumps(order_response)))
            
        conn.commit()
        print(f"Order saved successfully for {symbol}")
        
    except Exception as e:
        print(f"Error saving order({symbol}): {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def save_pair(symbol, base_asset, quote_asset):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO usdt_pairs (symbol, base_asset, quote_asset)
            VALUES (%s, %s, %s)
            """, (symbol, base_asset, quote_asset))
            
        conn.commit()
        print(f"Pair {symbol} saved successfully")
        
    except Exception as e:
        print(f"Error saving pair({symbol}): {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_table():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usdt_pairs (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                symbol TEXT UNIQUE,
                base_asset TEXT,
                quote_asset TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("USDT pairs table created successfully")
        conn.commit()
        
    except Exception as e:
        print(f"Error creating table: {e}")
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()