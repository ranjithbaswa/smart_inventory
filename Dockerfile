FROM python:3.12-slim

# Ensure logs show immediately
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install Python dependencies
COPY smart_inventory_be/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY smart_inventory_be/ /app/

