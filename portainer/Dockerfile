FROM portainer/portainer-ce:alpine

RUN apk --update --no-cache add curl && rm -rf /var/cache/apk/*

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=3 CMD curl --fail http://127.0.0.1:9000/api/status || exit 1