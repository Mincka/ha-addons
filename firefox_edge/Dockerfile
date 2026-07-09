FROM jlesage/firefox:v26.07.1

RUN apk del firefox
RUN sed -r -i -e 's/v[0-9]+\.[0-9]+/edge/g' /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add firefox

COPY rootfs/startapp.sh /startapp.sh
# Ship a Home Assistant-tolerant tmp-clear init script. The stock upstream
# script aborts container init when it cannot remove the supervisor's
# read-only/busy bind-mounts (pulse.sock, cid) under /tmp/run.
COPY rootfs/etc/cont-init.d/08-clear-tmp-dir.sh /etc/cont-init.d/08-clear-tmp-dir.sh
# Makes sure that the line endings are correct
RUN sed -i 's/\r$//' /startapp.sh /etc/cont-init.d/08-clear-tmp-dir.sh
RUN chmod +x /startapp.sh /etc/cont-init.d/08-clear-tmp-dir.sh