# Use the official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements (Flask)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code
COPY app.py .

# Expose port
EXPOSE 5000

# Command to run the API
CMD ["python", "app.py"]
