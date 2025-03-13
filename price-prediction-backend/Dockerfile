# Use the official Python image from the Docker Hub
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI script and model file into the container
COPY server.py .
COPY xgb_model.pkl .

# Expose the port that the app runs on
EXPOSE 5500

# Command to run the FastAPI app
CMD ["python", "server.py"]