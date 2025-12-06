FROM python:3.12-slim

# Avoids Python buffering
ENV PYTHONUNBUFFERED 1

# Set a working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

