FROM python:3.8-slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by TensorFlow
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    libhdf5-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3-dev \
    python3-pandas \
    python3-sklearn \
    python3-yaml \
    python3-redis \
    # Consider if a system package exists for google-cloud-storage
    # If not, you'll still need pip for it.
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



# Install system dependencies required by TensorFlow

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -e .

# Train the model before running the application
RUN python pipeline/training_pipeline.py

# Expose the port that Flask will run on
EXPOSE 5001

# Command to run the app
CMD ["python", "application.py"]


