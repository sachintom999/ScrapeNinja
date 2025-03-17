# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y redis-tools

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

CMD ["scrapy", "crawl", "101", "--loglevel", "ERROR"]

