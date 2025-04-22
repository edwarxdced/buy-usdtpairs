from db.connection import get_connection


def create_tables() -> None:
    """
    Create the tables in the database.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usdt_pairs (
            symbol VARCHAR(50) PRIMARY KEY,
            base_asset VARCHAR(20) NOT NULL,
            quote_asset VARCHAR(20) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(50),
            quantity DOUBLE,
            price DOUBLE,
            usdt_amount DOUBLE,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        print("✅ MySQL tables created successfully.")
