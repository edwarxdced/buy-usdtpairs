# 🧠 Binance USDT Trading Bot

An automated trading bot that detects newly listed `USDT` pairs on Binance and executes market buy orders using a configurable amount.

---

## 🚀 Features

- ✅ Secure connection to Binance API
- ✅ Automatically detects new `USDT` trading pairs
- ✅ Executes `MARKET` buy orders
- ✅ Validates Binance filters (step size, notional)
- ✅ Saves trades and symbols in MySQL database
- ✅ Sends notifications via Telegram
- ✅ Modular and maintainable codebase

---

## 📁 Project Structure

```
buy-usdtpairs/
├── setup_db.py               # Initializes DB tables and seeds first trading pairs
├── main.py                   # Main script: checks and buys new trading pairs
├── config.py                 # Loads environment variables and config values
├── .env.example              # Example file for environment variables
├── db/
│   ├── connection.py         # MySQL database connection
│   ├── create_tables.py      # Table creation script (alternative to setup)
│   └── db_handler.py         # CRUD operations for database
├── utils/
│   ├── logger.py             # Centralized logging configuration
│   ├── trading.py            # Order validation and trading calculations
│   └── filter_pairs.py       # Filters symbols by quote asset and status
├── enums/
│   └── order.py              # Enums for order types and sides
```

---

## ⚙️ Requirements

- Python 3.10+
- MySQL Server
- Binance account with API access
- Telegram bot and chat ID for notifications

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=usdt_trading_bot

TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id

AMOUNT_BUY=10
PAIR_QUOTE=USDT
```

---

## 🛠️ Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create database tables and seed initial pairs

```bash
python setup_db.py
```

### 3. Run the trading bot

```bash
python main.py
```

---

## 📊 Technical Notes

- The bot validates:
  - `LOT_SIZE` (step size)
  - `NOTIONAL` (minimum total value of the order)
- Orders that don't meet Binance trading rules are skipped.
- Logs are printed to the console and can be integrated with any logging system.

---

## 📌 Why this project matters

This bot demonstrates:

- Type hinting and typing best practices
- SOLID design principles
- Clean separation of concerns (config, DB, business logic, APIs)
- Real-world API integration and error handling
- Financial process automation

---

## 📬 Author

Developed by [Edwar Cedeño](https://www.linkedin.com/in/edwar-cedeno/)  
💼 Backend Developer | Python | Fintech & Crypto


## ⚠️ Disclaimer

This project is created solely for educational purposes and knowledge sharing.  
It is not intended for use in live trading with real funds unless properly tested, audited, and adapted to your specific risk management needs.  
The author is not responsible for any financial loss resulting from the use of this code.

Use at your own risk.