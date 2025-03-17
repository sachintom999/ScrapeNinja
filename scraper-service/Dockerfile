# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose any required ports (if needed)
EXPOSE 9000  

# Set environment variables (if needed)
ENV PYTHONUNBUFFERED=1

# Define the command to start the Scrapy spider with Kafka consumer
CMD ["scrapy", "crawl", "my_spider"]
