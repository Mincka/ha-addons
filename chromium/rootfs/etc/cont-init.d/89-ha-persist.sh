#!/bin/sh
#
# Remap Chromium's folders onto Home Assistant's persistent storage.
#
# This runs during container init (as root), before the app service drops to
# the unprivileged application user. Doing the remap here — instead of in
# startapp.sh — lets Chromium run as a non-root user, which is required for its
# sandbox to work (Chromium refuses to run sandboxed as root, crbug.com/638180).
#
# The container's /config is not persistent on Home Assistant, so the profile
# is moved to /data (which is) and downloads are sent to the shared /share
# folder. Both are symlinked back into /config where Chromium expects them.
#

set -e # Exit immediately if a command exits with a non-zero status.
set -u # Treat unset variables as an error.

APP_UID="${USER_ID:-1000}"
APP_GID="${GROUP_ID:-1000}"

# Persist the Chromium profile to /data.
if [ ! -d /data/chromium ]; then
    if [ -d /config/chromium ] && [ ! -L /config/chromium ]; then
        # First run: keep the profile the base image just created.
        mv /config/chromium /data/chromium
    else
        mkdir -p /data/chromium
    fi
fi
rm -rf /config/chromium
ln -s /data/chromium /config/chromium

# Persist downloads to the shared /share/chromium folder.
mkdir -p /share/chromium
rm -rf /config/Downloads
ln -s /share/chromium /config/Downloads

# The application runs unprivileged, so make sure it owns its persisted data.
chown -h "$APP_UID:$APP_GID" /config/chromium /config/Downloads
chown -R "$APP_UID:$APP_GID" /data/chromium /share/chromium

# vim:ft=sh:ts=4:sw=4:et:sts=4
