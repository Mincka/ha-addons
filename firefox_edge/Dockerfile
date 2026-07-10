FROM jlesage/firefox:v26.07.1

RUN apk del firefox
RUN sed -r -i -e 's/v[0-9]+\.[0-9]+/edge/g' /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add firefox

# Ship a Home Assistant-tolerant tmp-clear init script. The stock upstream
# script aborts container init when it cannot remove the supervisor's
# read-only/busy bind-mounts (pulse.sock, cid) under /tmp/run.
COPY rootfs/etc/cont-init.d/08-clear-tmp-dir.sh /etc/cont-init.d/08-clear-tmp-dir.sh
# Update Firefox from Alpine edge on every startup (runs as root at init).
COPY rootfs/etc/cont-init.d/50-update-firefox.sh /etc/cont-init.d/50-update-firefox.sh
# Remap Firefox's profile and downloads onto Home Assistant's persistent
# storage during init (as root), so Firefox itself can run unprivileged.
COPY rootfs/etc/cont-init.d/89-ha-persist.sh /etc/cont-init.d/89-ha-persist.sh
# Makes sure that the line endings are correct
RUN sed -i 's/\r$//' /etc/cont-init.d/08-clear-tmp-dir.sh /etc/cont-init.d/50-update-firefox.sh /etc/cont-init.d/89-ha-persist.sh
RUN chmod +x /etc/cont-init.d/08-clear-tmp-dir.sh /etc/cont-init.d/50-update-firefox.sh /etc/cont-init.d/89-ha-persist.sh
