import psycopg2
from termcolor import cprint

# PostgreSQL connection details
DB_NAME = "foundry_db"
DB_USER = "foundry_user"
DB_PASSWORD = "foundry_password"
DB_HOST = "localhost"  # Change if your DB is hosted elsewhere
DB_PORT = "5432"       # Default PostgreSQL port

try:
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    
    # Truncate the table
    cursor.execute("TRUNCATE TABLE quotes RESTART IDENTITY CASCADE")
    conn.commit()
    
    cprint("Table 'quotes' truncated successfully!", "green")

except Exception as e:
    cprint(f"Error: {e}", "red")

finally:
    cursor.close()
    conn.close()
