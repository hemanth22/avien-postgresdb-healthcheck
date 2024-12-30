import psycopg2
from psycopg2 import OperationalError
import json
import logging
from uuid import uuid4
from datetime import datetime
import pytz
import os


DB_HOST = os.environ.get('postgres_hostname')
DB_NAME = os.environ.get('postgres_database')
DB_PORT = os.environ.get('postgres_port')
DB_USER = os.environ.get('postgres_username')
DB_PASSWORD = os.environ.get('postgres_password')

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def log_json(status, message, details=None):
    """
    Log the heartbeat result in JSON format.
    :param status: Status of the heartbeat (e.g., "OK" or "FAILED").
    :param message: A short description of the result.
    :param details: Optional additional details (e.g., error message).
    """
    # Get the current IST time
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_timestamp = datetime.now(ist_timezone).isoformat()

    log_entry = {
        "uuid": str(uuid4()),  # Unique identifier for the log entry
        "timestamp": ist_timestamp,  # IST timestamp
        "status": status,
        "message": message,
        "details": details
    }
    logger.info(json.dumps(log_entry))

def check_database_connection(config):
    """
    Function to check the PostgreSQL database connection.
    :param config: Dictionary with database connection parameters.
    :return: None
    """
    try:
        # Connect to the database
        connection = psycopg2.connect(**config)
        cursor = connection.cursor()
        
        # Execute a simple query
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        if result:
            log_json(status="OK", message="Database heartbeat successful.")
        
        # Close the connection
        cursor.close()
        connection.close()
    except OperationalError as e:
        log_json(status="FAILED", message="Database heartbeat failed.", details=str(e))

if __name__ == "__main__":
    # Configuration for PostgreSQL database connection
    config = {
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT
    }
    
    # Perform a single heartbeat check
    check_database_connection(config)

