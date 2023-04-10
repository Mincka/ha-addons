FROM jlesage/firefox:v23.03.1

RUN apk del firefox
RUN sed -i -e 's/v3\.17/edge/g' /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add firefox

COPY rootfs/startapp.sh /startapp.sh
RUN chmod +x /startapp.sh
