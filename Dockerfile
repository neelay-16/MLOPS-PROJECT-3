FROM python:3.8-slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies required by TensorFlow
RUN pip install pandas google-cloud-storage scikit-learn PyYAML
    pip install pandas scikit-learn imbalanced-learn redis


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


