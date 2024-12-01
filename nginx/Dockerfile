FROM nginx:1.27-alpine-slim

# Install build dependencies
RUN apk add --no-cache \
    curl \
    gcc \
    libc-dev \
    make \
    openssl-dev \
    pcre-dev \
    zlib-dev \
    linux-headers \
    wget \
    git

# Get NGINX source and headers-more module
RUN cd /tmp && \
    wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && \
    tar zxf nginx-${NGINX_VERSION}.tar.gz && \
    git clone https://github.com/openresty/headers-more-nginx-module.git && \
    cd nginx-${NGINX_VERSION} && \
    ./configure \
        --with-compat \
        --add-dynamic-module=../headers-more-nginx-module && \
    make modules && \
    cp objs/ngx_http_headers_more_filter_module.so /etc/nginx/modules/ && \
    cd / && \
    rm -rf /tmp/*

# Clean up build dependencies
RUN apk del gcc libc-dev make openssl-dev pcre-dev zlib-dev linux-headers wget git

# Copy configuration
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./default.conf /etc/nginx/conf.d/default.conf

HEALTHCHECK --interval=1m30s --timeout=10s --start-period=40s --retries=3 CMD curl -so /dev/null http://localhost/ || exit 1