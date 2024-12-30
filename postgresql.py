import json
import psycopg2
import logging
import uuid
import subprocess
import os

DB_HOST = os.environ.get('postgres_hostname')
DB_NAME = os.environ.get('postgres_database')
DB_PORT = os.environ.get('postgres_port')
DB_USER = os.environ.get('postgres_username')
DB_PASSWORD = os.environ.get('postgres_password')

# Function to get IP addresses using hostname -I
def get_ip_addresses():
    try:
        output = subprocess.check_output(['hostname', '-I'])
        return output.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return f"Error retrieving IP addresses: {e}"

# Custom JSON Formatter for logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record),
            'message': record.getMessage(),
            'hostname': subprocess.check_output(['hostname']).decode('utf-8').strip(),
            'ip_addresses': get_ip_addresses(),
            'level': record.levelname,
            'uuid': str(uuid.uuid4()),
            
        }
        return json.dumps(log_record)

# Configure logging with JSONFormatter
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
json_handler = logging.StreamHandler()
json_handler.setFormatter(JSONFormatter())
logger.addHandler(json_handler)

# Database connection details


db_config = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT
}

# Connect to PostgreSQL database
def check_database_status():
    try:
        with psycopg2.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                logger.info("Database connection established.")
            
                #  Perform your database operations here
                cursor.execute("SELECT 1;")
                result = cursor.fetchone()
                if result:
                    logger.info(f"Database heartbeat successful")
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")

# Example function to log a message
def log_heartbeat_status():
    try:
        # Assuming a function or method checks the database status
        check_database_status()  # Replace with your actual function
    except Exception as e:
        logger.error(f"Database heartbeat failed: {e}")


log_heartbeat_status()
