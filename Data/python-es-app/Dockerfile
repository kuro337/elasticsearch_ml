# Use an official Python runtime as the base image
FROM python:3.12.0-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY ./elasticsearchpy/requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./elasticsearchpy /app

# Specify the command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "elasticsearchpy.wsgi:application"]
