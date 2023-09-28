# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Seed the database
RUN python ./api/models.py

# Make port 5000 available to the outside world
EXPOSE 5000

# Define the command to run the app using Flask's development server
CMD ["python", "./api/app.py"]

