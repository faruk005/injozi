# Use the official Python image as base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    FLASK_ENV=development \
    MONGO_URI=mongodb://localhost:27017/injozi

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host", "0.0.0.0"]
