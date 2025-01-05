import psycopg2  # type: ignore
import os
from datetime import datetime


# Database connection parameters
postgres_hostname = os.environ.get('postgres_hostname')
postgres_database = os.environ.get('postgres_database')
postgres_port = os.environ.get('postgres_port','5432')
postgres_username = os.environ.get('postgres_username')
postgres_password = os.environ.get('postgres_password')

def generate_fix_message(database_status):
    # Define the FIX protocol message structure and fields
    message = {
        "35": "A",  # Message Type (Logon)
        "49": "YOUR_COMPANY_ID",  # SenderCompID
        "56": "RECIPIENT_COMPANY_ID",  # TargetCompID
        "34": "12345",  # MsgSeqNum
        "52": datetime.now().strftime("%Y%m%d-%H:%M:%S"),  # SendingTime
        "DatabaseStatus": database_status  # Custom field
    }
    return message


try:
    # Establish a connection to the database
    conn = psycopg2.connect(
        database=postgres_database,
        user=postgres_username,
        password=postgres_password,
        host=postgres_hostname,
        port=postgres_port
        )
    # Generate a FIX protocol message indicating a successful connection
    fix_message = generate_fix_message("Connected")
    print(fix_message)
except psycopg2.Error as e:
    # Generate a FIX protocol message indicating a failed connection
    fix_message = generate_fix_message("Disconnected")
    print(fix_message)

