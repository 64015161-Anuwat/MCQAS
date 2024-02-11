import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="mcqas",
    user="postgres",
    password="admin123",
    host="localhost",
    port="5432"
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

try:
    # Query to get all table names
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

    # Fetch all rows from the result set
    tables = cursor.fetchall()

    # Iterate through each table and truncate it
    for table in tables:
        table_name = table[0]
        truncate_query = f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;'
        try:
            cursor.execute(truncate_query)
            print(f"Truncated table: {table_name}")
        except psycopg2.Error as e:
            print(f"Error truncating table {table_name}: {e}")

    # Commit your changes
    conn.commit()
    print("Changes committed successfully")

except psycopg2.Error as e:
    # If an error occurs, rollback the transaction
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Close communication with the PostgreSQL database
    cursor.close()
    conn.close()