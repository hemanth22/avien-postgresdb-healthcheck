import psycopg2  # type: ignore
import os
import logging
import json
import uuid
from datetime import datetime
import requests

# Custom JSON logging function
def log_json(level, message):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"),
        "message": message,
        "traceid": str(uuid.uuid4()),
    }
    logger.log(level, json.dumps(log_entry))

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Fetch environment variables
postgres_hostname = os.environ.get('postgres_hostname')
postgres_database = os.environ.get('postgres_database')
postgres_port = os.environ.get('postgres_port')
postgres_username = os.environ.get('postgres_username')
postgres_password = os.environ.get('postgres_password')
bot_token = os.environ.get('Priyoid_bot')
conn = None


def telegram_send_message(message):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id=-1002266504611&text={}".format(bot_token, message)
    requests.get(url)

def heartbeat():
    try:
        # Establishing the connection
        log_json(logging.INFO, "Attempting to connect to the PostgreSQL database...")
        conn = psycopg2.connect(
            database=postgres_database,
            user=postgres_username,
            password=postgres_password,
            host=postgres_hostname,
            port=postgres_port
        )

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        log_json(logging.INFO, "Cursor created successfully.")

        # Executing a PostgreSQL function using the execute() method
        cursor.execute("SELECT message FROM heartbeats;")
        log_json(logging.INFO, "Executed query: SELECT version()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        log_json(logging.INFO, f"Connection established to: {data}")
        log_json(logging.INFO, "Database heartbeat is successful.")

        if data:
            telegram_send_message(f"Database heartbeat is successful.")
            return data
        if not data:
            telegram_send_message(f"Database heartbeat is unsuccessful.")

    except psycopg2.Error as e:
        log_json(logging.ERROR, f"An error occurred while connecting to the database: {e}")

    finally:
        # Closing the connection
        if conn:
            conn.close()
            log_json(logging.INFO, "Database connection closed, will connect in next run")
        if not conn:
            log_json(logging.ERROR, "Database connection not established, kindly investigate the issue")

heartbeat()