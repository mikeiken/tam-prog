# Build stage
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

ENV NODE_ENV=production
ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package*.json ./

RUN npm install --production --silent && \
    npm cache clean --force

COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine-slim

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets
COPY --from=builder /usr/src/app/build /usr/share/nginx/html

# Set permissions and install curl
RUN chmod -R 755 /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    apk add --no-cache curl && \
    rm -rf /var/cache/apk/*

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/index.html || exit 1

CMD ["nginx", "-g", "daemon off;"]