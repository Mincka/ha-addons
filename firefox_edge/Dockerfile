FROM jlesage/firefox:v23.05.2

RUN apk del firefox
RUN sed -r -i -e 's/v[0-9]+\.[0-9]+/edge/g' /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add firefox

COPY rootfs/startapp.sh /startapp.sh
RUN chmod +x /startapp.sh