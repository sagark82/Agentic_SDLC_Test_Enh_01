#!/bin/bash

echo "Deploying Pharma Inc. Website..."

# Ensure the web server directory exists
mkdir -p /var/www/pharma-inc

# Copy all frontend files
echo "Copying website files..."
cp *.html /var/www/pharma-inc/
cp -r css /var/www/pharma-inc/
cp -r js /var/www/pharma-inc/

# Start the backend server (using a process manager like gunicorn in a real scenario)
echo "Starting backend server..."
nohup python app.py &

echo "Deployment complete."
