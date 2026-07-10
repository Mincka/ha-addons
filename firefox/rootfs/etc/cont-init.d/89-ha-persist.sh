#!/bin/sh
#
# Remap Firefox's folders onto Home Assistant's persistent storage.
#
# This runs during container init (as root), before the app service drops to
# the unprivileged application user. Doing the remap here — instead of in
# startapp.sh — lets Firefox run as a non-root user.
#
# The container's /config is not persistent on Home Assistant, so the profile
# is moved to /data (which is) and downloads are sent to the shared /share
# folder. Both are symlinked back into /config where Firefox expects them.
#

set -e # Exit immediately if a command exits with a non-zero status.
set -u # Treat unset variables as an error.

APP_UID="${USER_ID:-1000}"
APP_GID="${GROUP_ID:-1000}"

# Persist the Firefox profile to /data.
if [ ! -d /data/profile ]; then
    if [ -d /config/profile ] && [ ! -L /config/profile ]; then
        # First run: keep the profile the base image just created.
        mv /config/profile /data/profile
    else
        mkdir -p /data/profile
    fi
fi
rm -rf /config/profile
ln -s /data/profile /config/profile

# Persist downloads to the shared /share/firefox folder.
mkdir -p /share/firefox
rm -rf /config/downloads
ln -s /share/firefox /config/downloads

# The application runs unprivileged, so make sure it owns its persisted data.
chown -h "$APP_UID:$APP_GID" /config/profile /config/downloads
chown -R "$APP_UID:$APP_GID" /data/profile /share/firefox

# vim:ft=sh:ts=4:sw=4:et:sts=4
