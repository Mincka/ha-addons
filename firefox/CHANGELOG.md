<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

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
