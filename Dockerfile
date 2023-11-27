# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir paho-mqtt

# Expose the port the app runs on
EXPOSE 8081

# Run your Python script
CMD ["python", "app.py"]
