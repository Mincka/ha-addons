<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

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
