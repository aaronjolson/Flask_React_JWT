from datetime import datetime, timedelta
import secrets
from functools import wraps

from flask import Flask, request, jsonify, Response
import psycopg2
from passlib.hash import bcrypt
import jwt
from flask_cors import CORS

app = Flask(__name__)
app.debug = True

# Initialize CORS
CORS(app)

# Set up a secure hashing algorithm
pwd_context = bcrypt.using(rounds=12)
# Generate a random secret key with 32 bytes
SECRET_KEY = secrets.token_hex(32)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"message": "Missing or invalid authorization header"}), 401

        token = auth_header.split(' ')[1]

        try:
            # Decode and verify the JWT token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], verify=True)
            if datetime.utcnow() > datetime.fromtimestamp(decoded_token["exp"]):
                return jsonify({"message": "Token has expired"}), 401

            # Extract the username and email from the decoded token
            username = decoded_token.get('username')
            email = decoded_token.get('email')

            #TODO: check the token for additional info such as authorization levels
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.exceptions.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            print(e)
            return jsonify({"message": "Failed to decode or verify token"}), 401

        # Proceed with the original route handler
        return f(*args, **kwargs)

    return decorated


@app.route("/", methods=["GET"])
def hello():
    return "All Systems Functioning Normally."


@app.route("/signup", methods=["POST"])
def signup():
    # Retrieve the username, email, and password from the JSON body
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Remember to sanitize user inputs. Wouldn't hurt to do this on the SQL side as well.
    username = username.lower(),
    email = email.lower()

    # Create a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="db",
        port=5432,
        dbname="MYDATA",
        user="your_username",
        password="your_password"
    )

    # Create a cursor to interact with the database
    cur = conn.cursor()

    # Hash the password
    password_hash = pwd_context.hash(password)

    # Check if the username or email already exists in the database
    cur.execute("SELECT username, email FROM users WHERE username = %s OR email = %s", (username, email))
    existing_user = cur.fetchone()
    if existing_user:
        return Response("Username or email already exists", status=400)

    # Create a new row in the USERS table with the provided data
    cur.execute("INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, password_hash))

    # Commit the changes to the database and close the cursor
    conn.commit()
    cur.close()

    return jsonify({"message": "User created successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    # Retrieve the email and password from the JSON body
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # Create a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host="db",
        port=5432,
        dbname="MYDATA",
        user="your_username",
        password="your_password"
    )

    # Create a cursor to interact with the database
    cur = conn.cursor()

    # Retrieve the user's hashed password based on the provided email
    cur.execute("SELECT password_hash, username, email FROM users WHERE email = %s OR username = %s", (email, username))
    result = cur.fetchone()

    if result is None:
        return jsonify({"message": "Invalid email or password"}), 401

    stored_password_hash = result[0]
    username = result[1]
    email = result[2]

    # Verify the entered password against the stored hashed password
    if not pwd_context.verify(password, stored_password_hash):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate a JWT token for authentication
    payload = {
        "email": email,
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=1)  # Set the token expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "message": "Logged in successfully"}), 200


@app.route("/user", methods=["GET"])
@requires_auth
def get_user_info():
    # Get the query parameter value (email or username) from the URL
    email = request.args.get("email")
    username = request.args.get("username")

    # Check if the query parameter is provided
    if not email or username:
        return jsonify({"message": "Query parameter 'email' or 'username' is required"}), 400

    conn = psycopg2.connect(
        host="db",
        port=5432,
        dbname="MYDATA",
        user="your_username",
        password="your_password"
    )

    # Create a cursor to interact with the database
    cur = conn.cursor()
    if email:
        email = email.lower()
    elif username:
        username = username.lower()

    # Retrieve the user information based on the email or username
    cur.execute("SELECT * FROM users WHERE email = %s OR username = %s", (email, username))
    result = cur.fetchone()

    if result is None:
        return jsonify({"message": "User not found"}), 404

    # Extract the user information from the database result
    user_info = {
        "username": result[0],
        "email": result[1],
        # Include other relevant user information
    }

    return jsonify({"userInfo": user_info}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
