FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY cloud_gaming_optimizer/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY cloud_gaming_optimizer/ .

# Expose port
EXPOSE 5000

# Set environment
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "web_app.py"]
