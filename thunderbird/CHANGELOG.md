<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.1.1

- Base image update: jlesage/docker-thunderbird to v26.08.2
- Updated baseimage to version 4.13.2.

## 1.1.0

- Base image update: jlesage/docker-thunderbird to v26.08.1
- Updated baseimage to version 4.13.1:
  - Host clipboard sync can now be controlled via environment variable and web
    UI toggle.
  - Improved reliability and security of the web interface.
  - Improved reliability and security of services.
- Added new environment variables:
  - WEB_HOST_CLIPBOARD_SYNC: Enable/disable synchronizing the host system
    clipboard with the application (Chromium-based browsers only).
  - WEB_AUTHENTICATION_ALLOW_INSECURE: Allow web authentication without
    SECURE_CONNECTION being enabled (not recommended, useful behind a reverse
    proxy that already terminates HTTPS).

## 1.0.0

- Initial Thunderbird add-on, based on jlesage/docker-thunderbird v26.07.1 (Thunderbird 151.0.1-r0).
- Persists the Thunderbird profile (mail accounts, local folders, settings) to `/data` and
  provides a `downloads` folder mapped to `/share/thunderbird` for saving attachments, so
  everything survives add-on updates and restarts.
- Runs Thunderbird as an unprivileged user (no extra capabilities needed).
- Ships a hardened AppArmor profile (capabilities scoped to what the init system and
  Thunderbird need, plus mount and ptrace rules) instead of running unconfined.
