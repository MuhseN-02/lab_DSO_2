#!/bin/bash

IMAGE_NAME="arithmetic-api"
CONTAINER_NAME="arithmetic-api-container"

# Function to build and deploy the Docker image
build_and_deploy() {
    echo "[*] Building Docker image..."
    docker build -t $IMAGE_NAME .
    echo "[*] Stopping existing container (if any)..."
    docker rm -f $CONTAINER_NAME 2>/dev/null
    echo "[*] Running new container..."
    docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
}

# Monitor changes in the current directory
echo "[*] Monitoring for code changes..."
while true; do
    inotifywait -e modify,create,delete -r .
    build_and_deploy
done
