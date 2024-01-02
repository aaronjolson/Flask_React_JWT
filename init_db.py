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
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(255) PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        password_hash VARCHAR(255),
        create_date DATE,
        last_login_date DATE
    )
""")

# Create UPLOADS table
cur.execute("""
    CREATE TABLE IF NOT EXISTS uploads (
        upload_id VARCHAR(255) PRIMARY KEY,
        upload_name VARCHAR(255),
        user_id VARCHAR(255) REFERENCES users(username),
        upload_date DATE,
        file_location VARCHAR(255),
        file_size FLOAT
    )
""")

# Create LIKES table
cur.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        user_id VARCHAR(255) REFERENCES users(username),
        image_id VARCHAR(255) REFERENCES uploads(upload_id)
    )
""")

# Create CATEGORIES table
cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id VARCHAR(255) PRIMARY KEY,
        category_name VARCHAR(255)
    )
""")

# Create IMAGE_CATEGORIES table
cur.execute("""
    CREATE TABLE IF NOT EXISTS image_categories (
        category_id VARCHAR(255) REFERENCES categories(category_id),
        image_id VARCHAR(255) REFERENCES uploads(upload_id)
    )
""")

# Commit the changes to the database and close the cursor
conn.commit()
cur.close()
conn.close()
