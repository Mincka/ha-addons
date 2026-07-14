<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.1.0

- Base image update: jlesage/docker-chromium to v26.07.2.
  - Updated Chromium to version 150.0.7871.114-r0.
  - Updated baseimage to version 4.12.6, bringing the following changes:
    - Fixed regression causing container startup failure when the container engine
      automatically mounts files under `/run`.
    - Read-only filesystem support now requires exposing `/run` as a tmpfs.

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
