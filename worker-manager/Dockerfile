# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variables (if needed)
ENV PYTHONUNBUFFERED=1

# Run the worker manager script
CMD ["python", "main.py"]
