#!/bin/sh
#
# Update Firefox from the Alpine edge repository on every startup.
#
# This runs during container init (as root), before the app service drops to
# the unprivileged application user. Running it here — instead of in
# startapp.sh — is what lets this "edge" variant run the browser non-root while
# still refreshing Firefox on each start.
#
# Best-effort: a failed upgrade (e.g. no network) must not prevent the add-on
# from starting; it just keeps the Firefox version baked into the image.
#

set -u

echo "[firefox-edge] Updating Firefox from Alpine edge..."
if apk update && apk upgrade; then
    echo "[firefox-edge] Firefox is up to date."
else
    echo "[firefox-edge] WARNING: apk upgrade failed; keeping the current Firefox version." >&2
fi

exit 0

# vim:ft=sh:ts=4:sw=4:et:sts=4
