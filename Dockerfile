
# Use an official Python runtime as a parent image
FROM python:3.9-slim


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


FROM ubuntu:latest

# Install required packages including libgobject
RUN apt-get update && apt-get install -y \
    libgobject-2.0-0 \
    libglib2.0-dev \
    libgirepository1.0-dev \
    python3-gi \
    && apt-get clean


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
