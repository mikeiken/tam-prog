FROM nginx:1.27-alpine-slim

# Install curl for healthcheck
RUN apk add --no-cache curl

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

HEALTHCHECK --interval=1m30s --timeout=10s --start-period=40s --retries=3 CMD curl -so /dev/null http://localhost/ || exit 1