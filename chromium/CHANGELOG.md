<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.4.0

- Base image update: jlesage/docker-chromium to v26.08.3.
  - Updated Chromium to version 151.0.7922.173-r0.

## 1.3.1

- Base image update: jlesage/docker-chromium to v26.08.2.
  - Updated baseimage to version 4.13.2.

## 1.3.0

- Base image update: jlesage/docker-chromium to v26.08.1.
  - Updated Chromium to version 151.0.7922.108-r0.
  - Updated baseimage to version 4.13.1, bringing the following changes:
    - Host clipboard sync can now be controlled via environment variable and
      web UI toggle.
    - Improved reliability and security of the web interface.
    - Improved reliability and security of services.
- Added new environment variables:
  - WEB_HOST_CLIPBOARD_SYNC: Enable/disable synchronizing the host system
    clipboard with the application (Chromium-based browsers only).
  - WEB_AUTHENTICATION_ALLOW_INSECURE: Allow web authentication without
    SECURE_CONNECTION being enabled (not recommended, useful behind a reverse
    proxy that already terminates HTTPS).

## 1.2.0

- Base image update: jlesage/docker-chromium to v26.07.3.
  - Updated Chromium to version 150.0.7871.128-r0.
  - Added Chromium language packs.

## 1.1.0

- Base image update: jlesage/docker-chromium to v26.07.2.
  - Updated Chromium to version 150.0.7871.114-r0.
  - Updated baseimage to version 4.12.6, bringing the following changes:
    - Fixed regression causing container startup failure when the container engine
      automatically mounts files under `/run`.
    - Read-only filesystem support now requires exposing `/run` as a tmpfs.
- Removed the add-on's custom tmp-clear init script. It worked around the
  v26.07.1 startup failure on Home Assistant's bind-mounts, which baseimage
  4.12.6 now fixes upstream, so the stock script is used again.

## 1.0.0

- Initial Chromium add-on, based on jlesage/docker-chromium v26.07.1 (Chromium 149.0.7827.200-r0).
- Persists the Chromium profile to `/data` and stores downloads in `/share/chromium` so they
  survive add-on updates and restarts.
- Runs Chromium with its sandbox enabled (via the `SYS_ADMIN` capability), avoiding the
  `--no-sandbox` fallback and its "unsupported command-line flag" infobar.
- Ships a Home Assistant-tolerant tmp-clear init script so the add-on starts cleanly under the
  supervisor's `/tmp/run` bind-mounts.
- Ships a hardened AppArmor profile (capabilities scoped to what the init system and the
  Chromium sandbox need, plus mount and ptrace rules) instead of running unconfined.
