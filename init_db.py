import psycopg2

# Database configuration
db_host = "localhost"
db_port = 5432
db_name = "MYDATA"
db_user = "your_username"
db_password = "your_password"

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Create USERS table
cur.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        create_date DATE,
        last_login_date DATE
    )
""")

# Commit the changes to the database and close the cursor
conn.commit()
cur.close()
conn.close()
