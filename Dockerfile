# Use the official Python image from the Docker Hub
FROM --platform=linux/arm64 python:3.11

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for ARM64
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libv4l-0 \
    v4l-utils \
    udev \
    && rm -rf /var/lib/apt/lists/*

# Add root user to video group (group already exists)
RUN usermod -a -G video root

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]