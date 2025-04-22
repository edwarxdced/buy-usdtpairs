import logging
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import Any, Dict, Union

import mysql.connector
from mysql.connector import CMySQLConnection

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER

DbData = Union[Decimal, bytes, date, datetime, float, int, str, time, timedelta, None]
DbConfig = Dict[str, Any]

db_config: DbConfig = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
}

logger = logging.getLogger(__name__)


def get_connection() -> CMySQLConnection:
    """
    Get a connection to the database.

    Returns:
        CMySQLConnection: A connection to the database.
    """
    try:
        conn = mysql.connector.connect(**db_config)
        if not isinstance(conn, CMySQLConnection):
            raise TypeError("Expected CMySQLConnection")
        return conn
    except mysql.connector.Error as err:
        logger.error(f"MySQL connection error: {err}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
