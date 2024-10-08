# Use the official Python image from the Alpine version
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install dependencies
RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev openssl-dev make postgresql-dev curl

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the application will run on
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD curl --fail http://localhost:8000/admin || exit 1

# Run migrations and start the Django development server
CMD ["sh", "-c", "python tamprog/manage.py makemigrations && python tamprog/manage.py migrate && python tamprog/manage.py runserver 0.0.0.0:8000"]