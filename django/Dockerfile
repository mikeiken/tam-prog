# Build stage
FROM python:3.9-alpine as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install build dependencies and compile requirements
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    make \
    postgresql-dev \
    && pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install only runtime dependencies
RUN apk add --no-cache libpq curl

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy only necessary project files
COPY tamprog/ tamprog/
COPY entrypoint.sh .

# Collect static files and clean up in single layer
RUN python tamprog/manage.py collectstatic --noinput \
    && find . -type d -name __pycache__ -exec rm -r {} + \
    && rm -rf /root/.cache /tmp/*

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD curl --fail http://localhost:8000/admin || exit 1

WORKDIR /usr/src/app/tamprog

ENTRYPOINT ["/bin/sh", "../entrypoint.sh"]