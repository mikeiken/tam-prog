FROM nginx:1.27-alpine-slim
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
HEALTHCHECK --interval=1m30s --timeout=10s --start-period=40s --retries=3 CMD service nginx status