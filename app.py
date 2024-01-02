from datetime import datetime, timedelta
import io
import uuid
import secrets
from functools import wraps

from flask import Flask, request, jsonify, Response, send_file, abort
import psycopg2
from passlib.hash import bcrypt
import boto3
from botocore.exceptions import ClientError
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
    cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
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
    cur.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
    result = cur.fetchone()

    if result is None:
        return jsonify({"message": "Invalid email or password"}), 401

    stored_password_hash = result[0]

    # Verify the entered password against the stored hashed password
    if not pwd_context.verify(password, stored_password_hash):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate a JWT token for authentication
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=1)  # Set the token expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "message": "Logged in successfully"}), 200


@app.route("/logout", methods=["POST"])
def logout():
    #TODO invalidate the jwt in the header

    return jsonify({"message": "Logout successful"}), 200


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


@app.route("/getImage/<imageId>", methods=["GET"])
def get_image(imageId):
    try:
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

        # Retrieve the file URL from the IMAGES table based on the imageId
        cur.execute("SELECT file_location FROM images WHERE image_id = %s", (imageId,))
        result = cur.fetchone()

        if result is None:
            return jsonify({"message": "Image not found"}), 404

        file_location = result[0]

        try:
            # Connect to Amazon S3
            s3 = boto3.client(
                "s3",
                aws_access_key_id="your_aws_access_key",
                aws_secret_access_key="your_aws_secret_access_key"
            )
            # Retrieve the image from S3
            response = s3.get_object(Bucket="your_bucket_name", Key=file_location)
            image_data = response["Body"].read()

            # Set the appropriate content type based on the file extension
            content_type = response["ContentType"]

            # Return the image file as a response
            return send_file(
                io.BytesIO(image_data),
                mimetype=content_type,
                as_attachment=False
            )
        except ClientError as e:
            print(e)
            return abort(500)
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to retrieve image"}), 500


@app.route("/upload", methods=["POST"])
def upload():
    # Retrieve the file from the request
    file = request.files["file"]

    # Connect to Amazon S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id="your_aws_access_key",
        aws_secret_access_key="your_aws_secret_access_key"
    )

    try:
        # Upload the file to S3 bucket
        bucket_name = "your_bucket_name"
        s3.upload_fileobj(file, bucket_name, file.filename)

        # Get the URL of the uploaded file on S3
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"

        # Create a new row in the IMAGES table with the file details
        upload_id = str(uuid.uuid4())
        upload_name = file.filename
        upload_date = datetime.now().date()
        file_location = s3_url
        file_size = file.content_length

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

        cur.execute("""
            INSERT INTO images (upload_id, upload_name, upload_date, file_location, file_size)
            VALUES (%s, %s, %s, %s, %s)
        """, (upload_id, upload_name, upload_date, file_location, file_size))

        # Commit the changes to the database and close the cursor
        conn.commit()
        cur.close()

        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "File upload failed"}), 500


@app.route("/deleteImage", methods=["POST"])
def deleteImage():
    # Retrieve the imageId from the JSON body
    data = request.json
    image_id = data.get("imageId")

    try:
        # Create a connection to the PostgreSQL database
        conn = psycopg2.connect(
            host="db",
            port=5432,
            dbname="MYDATA",
            user="your_username",
            password="your_password"
        )

        s3 = boto3.client(
            "s3",
            aws_access_key_id="your_aws_access_key",
            aws_secret_access_key="your_aws_secret_access_key"
        )

        # Create a cursor to interact with the database
        cur = conn.cursor()

        # Delete the image from S3
        cur.execute("SELECT file_location FROM images WHERE image_id = %s", (image_id,))
        result = cur.fetchone()

        if result is None:
            return jsonify({"message": "Image not found"}), 404

        file_location = result[0]

        s3.delete_object(Bucket="your_bucket_name", Key=file_location)

        # Delete the image data from the database
        cur.execute("DELETE FROM images WHERE image_id = %s", (image_id,))

        # Commit the changes to the database and close the cursor
        conn.commit()
        cur.close()

        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to delete image"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
