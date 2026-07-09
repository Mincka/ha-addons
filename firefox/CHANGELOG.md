<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.11.1

- Fixed the add-on failing to start on upstream v26.07.1 (baseimage 4.12.5). The
  new baseimage relocated its runtime dir under `/tmp/run`, and its tmp-clear
  init script aborted container startup when it could not remove the Home
  Assistant supervisor's bind-mounts there (the read-only PulseAudio socket and
  the in-use container-id file), failing with "Read-only file system" /
  "Resource busy". The tmp-clear script is now tolerant of those mounts.

## 1.11.0

- Base image update: jlesage/docker-firefox to v26.07.1
- Updated Firefox to version 151.0.3-r0.
- Updated baseimage to version 4.11.3 (v26.03.1), then 4.12.5 (v26.07.1):
  - Enabled xcompmgr output only when debug is enabled.
  - Enhanced self-signed certificates by including the Subject Alternative Name (SAN) and using the container hostname instead of a dummy domain name.
  - Added the ability to run the container with a read-only filesystem.
  - Added the ability to configure the shell used by the web terminal.
  - Enabled window shadows to improve support of GTK4 applications.
  - Switched to fastcompmgr as the X compositor.
  - Updated TigerVNC to version 1.16.2.
  - Updated noVNC to version 1.7.0.
  - Improved web authentication compatibility with reverse proxies by using relative redirects.
  - Force usage of the local X display to avoid connecting to the host X server in Docker host network mode.
- Added new environment variable:
  - WEB_TERMINAL_SHELL_PATH: Configure the shell used by the web terminal

## 1.10.1

- Base image update: jlesage/docker-firefox to v26.02.3
- Updated baseimage to version 4.11.2:
  - Fixed X server failing to find the appropriate Mesa driver on some setups.

## 1.10.0

- Base image update: jlesage/docker-firefox to v26.02.2
- Updated baseimage to version 4.11.0 (v26.02.1), then 4.11.1 (v26.02.2):
  - Added a web terminal providing shell access to the container.
  - Fixed audio being paused when switching to another browser tab.
  - Web file manager is now displayed in a modal window.
  - Fixed file manager failures when uploading zero-byte files.
  - Fixed upload interruptions from interfering with other uploads.
  - Enhanced file manager error reporting accuracy.
  - Improved web services server stability and reliability.
  - Updated TigerVNC to 1.16.0 and X server to 21.1.21.
  - Fixed issue where taking ownership of directory would fail.
- Added new environment variable:
  - WEB_TERMINAL: Enable access to a terminal from the web interface

## 1.9.1

- Base image update: jlesage/docker-firefox to v26.01.1
- Updated baseimage to version 4.10.6:
  - On Mac devices, fixed conversion of Command+<Key> shortcuts to the proper Alt+<Key> shortcuts for Linux applications.

## 1.9.0

- Base image update: jlesage/docker-firefox to v25.12.4 (Firefox 145.0.1-r0)
- Added new environment variables:
  - WEB_FILE_MANAGER_ALLOWED_PATHS: Configure paths accessible through the web file manager
  - WEB_FILE_MANAGER_DENIED_PATHS: Configure paths blocked from web file manager access
  - WEB_AUTHENTICATION_TOKEN_VALIDITY_TIME: Configure authentication token lifetime (in hours)

## 1.8.1

- Fix FF_CUSTOM_ARGS default value from "0" to empty string.

## 1.8.0

- Base image update: jlesage/docker-firefox to v25.12.3 (Firefox 145.0-r0)
- Baseimage updated to version 4.10.3:
  - Fixed desktop notification forwarding service issues related to clients and WebSocket management.
  - Use Firefox native notification backend when web notification support is disabled.
- Clipboard synchronization now works with HA Ingress (copy/paste between host and Firefox).

## 1.7.0

- Base image update: jlesage/docker-firefox to 25.12.1
- Updated baseimage to version 4.10.1, which brings the following changes:
  - Added hardware acceleration support for the X server.
  - Added seamless clipboard synchronization for Chromium-based browsers. HA Add-on: Sadly, this does not seem to work as HA add-on with ingress, even if the add-on iframe is directly loaded over HTTPS.
  - Added web notification service to forward desktop notifications to the browser. HA Add-on: Not tested, may not work as HA add-on with ingress.
  - Added the ability to restrict web and VNC connections from localhost only.
  - Added web server support for TLS 1.3.
  - Removed web server support of static Diffie-Hellman parameters file (no longer needed in modern TLS configurations and ECDHE).

## 1.6.0

- Base image update: jlesage/docker-firefox to 25.07.2 (Firefox 114.0.4-r1)
  - Added automatic reconnect support of the web interface.
  - Added web file manager (https://github.com/jlesage/docker-baseimage-gui?tab=readme-ov-file#web-file-manager).
  - Do not ask VNC password when accessing the web interface and web authentication is enabled.
  - Misc updates and bug fixes

## 1.5.0

- Base image update: jlesage/docker-firefox to 25.03.1 (Firefox 136.0-r0)

## 1.4.0

- Base image update: jlesage/docker-firefox to 24.12.1 (Firefox 133.0-r0)
- Changes from jlesage's baseimage:
  - Fixed web audio feature with URL path-based reverse proxy.
  - Fixed TLS secure connection method for VNC that was preventing web access.
  - Fixed CJK font installation.
  - Rebuild against latest distro images to get security fixes.

## 1.3.2

- Base image update: jlesage/docker-firefox to 24.09.1 (Firefox 130.0.1-r0)
- Option to enable audio support through web browser (when you expose the addon with a dedicated web port). Not working with Ingress.
- HA Addon Audio support enabled for the host (not tested).
- Remote Debugging Port added.
- Option to enable Web authentication support.
- Option to set custom arguments for Firefox.

## 1.2.0

- Base image update: jlesage/docker-firefox to 24.04.1 (Firefox 124.0.1-r0)

## 1.1.0

- Base image update: jlesage/docker-firefox to 23.11.3
- Allow exposing VNC and Web ports on the Home Assistant host. This enables Kiosk scenarios with Kiosk mode and default URL options. 
- Make the menu entry available to all users (panel_admin: false).
- Enable the "legacy" mode to use options as environment variables. Few examples of available options below:
- Option to set a VNC password.
- Option to set a default URL.
- Option to start Firefox in Kiosk mode.
- Option to enable Dark Mode.
- Option to add font WenQuanYi Zen Hei. Support for Chinese/Japanese/Korean characters.
- Option to set the resolution of the application.

## 1.0.7

- Base image update: jlesage/docker-firefox to 23.05.2
- Starting with this version, this add-on uses the same repository than the base image.
- A "Firefox (Edge)" add-on is now available. The Edge version uses Alpine Edge repository and attempts to update Firefox each time the container starts.

## 1.0.6

- Rebuild to upgrade Firefox to 113.0.2

## 1.0.5

- Base image update: jlesage/docker-firefox to 23.05.1

## 1.0.4

- Update package name format

## 1.0.0

- Initial release
