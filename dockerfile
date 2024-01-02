# Use the official Python image as the base image
FROM python:3.9-slim

# Install PostgreSQL development libraries and headers
RUN apt-get update \
    && apt-get install -y build-essential \
                          libpq-dev

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining app files to the container
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Set the entrypoint command to run the Flask app
CMD ["python", "app.py"]