FROM jlesage/thunderbird:v26.08.2

LABEL \
  org.opencontainers.image.title="Thunderbird Home Assistant Add-on" \
  org.opencontainers.image.description="Docker container for Thunderbird" \
  org.opencontainers.image.source="https://github.com/mincka/ha-addons" \
  org.opencontainers.image.licenses="MIT"

# Remap Thunderbird's profile and downloads onto Home Assistant's persistent
# storage during init (as root), so Thunderbird itself can run unprivileged.
COPY rootfs/etc/cont-init.d/89-ha-persist.sh /etc/cont-init.d/89-ha-persist.sh
# Makes sure that the line endings are correct
RUN sed -i 's/\r$//' /etc/cont-init.d/89-ha-persist.sh
RUN chmod +x /etc/cont-init.d/89-ha-persist.sh
