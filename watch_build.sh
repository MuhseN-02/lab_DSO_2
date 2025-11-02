#!/bin/bash

# Name of the Docker image
IMAGE_NAME="arithmetic-api"

# Folder to monitor
WATCH_DIR="./"

echo "Monitoring $WATCH_DIR for changes..."

# --- Updated loop starts here ---
while true; do
    # Watch for meaningful changes (ignore swap/temp files)
    inotifywait -e modify,create,delete -r --exclude '(\.swp$|\.tmp$|\.pyc$)' $WATCH_DIR

    # Check for new commits in Git
    git fetch origin main
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/main)
    if [ $LOCAL != $REMOTE ]; then
        echo "New commits detected. Pulling changes..."
        git pull origin main
    fi

    echo "Changes detected. Rebuilding Docker image..."
    docker build -t $IMAGE_NAME .

    # Stop any running container
    CONTAINER_ID=$(docker ps -q --filter ancestor=$IMAGE_NAME)
    if [ ! -z "$CONTAINER_ID" ]; then
        docker stop $CONTAINER_ID
        docker rm $CONTAINER_ID
    fi

    # Run new container
    docker run -d -p 5000:5000 $IMAGE_NAME
    echo "Docker container updated."

    # Push the image to Docker Hub
    docker tag $IMAGE_NAME muhsen02/$IMAGE_NAME:latest
    docker push muhsen02/$IMAGE_NAME:latest
    echo "Docker image pushed to Docker Hub."
done
# --- Updated loop ends here ---
