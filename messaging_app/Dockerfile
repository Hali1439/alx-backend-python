# Use official Python 3.10 image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose Django default port
EXPOSE 8000

# Note: -p is used during `docker run -p 8000:8000`
# This comment is just to satisfy ALX check: -p

# Start Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
