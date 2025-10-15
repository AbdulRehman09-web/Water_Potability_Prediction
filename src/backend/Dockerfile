FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

## Copy application code
COPY . .

# Make script executable
RUN chmod +x start.sh

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["./start.sh"]
