<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.2.0

- Base image update: jlesage/docker-thunderbird to v26.11.2
  - v26.11.2:
    - Updated baseimage to version 4.15.1:
      - Fixed issue that could affect application window display.
  - v26.11.1:
    - Updated baseimage to version 4.15.0:
      - Added web microphone support.
      - Added H.264 encoding support for a moving screen in the web interface.
      - Web audio sample rate is now 48000 Hz.
      - Web audio now skips near-silence.
      - The web interface now shows the browser's own mouse pointer.
      - Improved responsiveness of screen updates in the web interface.
      - Fixed one-pixel border showing above the main application window.
      - Fixed main window un-maximizing on Alt+drag.
      - Fixed web audio staying off after the web interface reconnects.
      - Fixed idle JPEG refresh delaying the next interaction.
- Added new environment variable:
  - WEB_MICROPHONE: When set to 1, microphone support is enabled, allowing audio
    captured by the browser to be used by the application.

## 1.1.4

- Reverted GPU hardware acceleration (`video: true`, added in 1.1.3): it brought
  no noticeable improvement and caused higher CPU usage and sluggishness on some
  hosts (#138). The add-on uses software rendering again, as in 1.1.2.

## 1.1.3

- GPU hardware acceleration: the add-on now requests video hardware access
  (`video: true`), so the X server can use the host GPU (`/dev/dri`) instead of
  software rendering (`llvmpipe`). Requires an open-source kernel driver
  (Intel `i915`, AMD `amdgpu` or `nouveau`); proprietary NVIDIA drivers are not
  supported. Hosts without a GPU are unaffected.

## 1.1.2

- Base image update: jlesage/docker-thunderbird to v26.09.1
- Updated baseimage to version 4.14.0:
  - The web interface can now be installed as an application on a computer or
    phone.
  - Fixed host clipboard synchronization disabling itself.

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
