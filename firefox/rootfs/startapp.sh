#!/bin/sh

set -e # Exit immediately if a command exits with a non-zero status.
set -u # Treat unset variables as an error.

export HOME=/config

CUSTOM_START="/config/custom-start.sh"

# Create custom start script if it does not exist
if [ ! -f "$CUSTOM_START" ]; then
  cat << 'EOF' > "$CUSTOM_START"
  
# Custom startup script
# This file is executed automatically if present.
EOF
  chmod +x "$CUSTOM_START"
fi

# Execute custom start script if executable
if [ -x "$CUSTOM_START" ]; then
  echo "Executing custom-start.sh..."
  "$CUSTOM_START" || echo "custom-start.sh exited with non-zero status, continuing"
fi

PIDS=

notify() {
    for N in $(ls /etc/logmonitor/targets.d/*/send)
    do
       "$N" "$1" "$2" "$3" &
       PIDS="$PIDS $!"
    done
}

# Verify support for membarrier.
if ! /usr/bin/membarrier_check 2>/dev/null; then
   notify "$APP_NAME requires the membarrier system call." "$APP_NAME is likely to crash because it requires the membarrier system call.  See the documentation of this Docker container to find out how this system call can be allowed." "WARNING"
fi

# Wait for all PIDs to terminate.
set +e
for PID in "$PIDS"; do
   wait $PID
done
set -e

# Symbolic links for persistent storage on HA
if [ ! -d "/data/profile" ]; then
  mv /config/profile /data
else
  rm -rf /config/profile
fi
ln -s /data/profile /config/profile

if [ ! -d "/share/firefox" ]; then
  mkdir -p /share/firefox
fi
rm -rf /config/downloads

ln -s /share/firefox /config/downloads

/usr/bin/firefox --version
exec /usr/bin/firefox "$@" >> /config/log/firefox/output.log 2>> /config/log/firefox/error.log
