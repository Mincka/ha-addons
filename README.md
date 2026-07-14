# Mincka's Home Assistant Add-ons Repository

## Installation

[![Add repository on my Home Assistant][repository-badge]][repository-url]

If you want to add the repository manually, please follow the procedure highlighted in the [Home Assistant website](https://home-assistant.io/hassio/installing_third_party_addons). Use the following URL to add this repository: https://github.com/mincka/ha-addons

## Add-ons provided by this repository

### [Firefox](./firefox)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

_Run Firefox as a browser inside Home Assistant to access local or external web sites from your home._

### [Firefox (Edge)](./firefox_edge)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

_Run Firefox as a browser inside Home Assistant to access local or external web sites from your home._

This _Edge_ version updates to the latest Firefox version on container start.

The startup speed of the Edge version's add-on tends to become progressively slower after each Firefox update, as it updates all installed packages, including Firefox, upon booting.

The Edge version can also be unstable because the compatibility with the VNC add-on is not tested with the latest Firefox version.

If you don’t need the very latest version of Firefox, it’s fine to stay on the standard version.

### [Chromium](./chromium)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

_Run Chromium as a browser inside Home Assistant to access local or external web sites from your home._

## Support
Got questions?

You have several options to get them answered:

- The Home Assistant [Community Forum](https://community.home-assistant.io/t/home-assistant-add-on-firefox/558672)
- This repository issues list

## Sponsoring ❤️
If you like this add-on and would like to support my work, you can buy me a coffee. ☕

Sponsoring available on GitHub (https://github.com/sponsors/Mincka) and Paypal (https://paypal.me/JulienEhrhart).

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[repository-badge]: https://img.shields.io/badge/Add%20repository%20to%20my-Home%20Assistant-41BDF5?logo=home-assistant&style=for-the-badge
[repository-url]: https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmincka%2Fha-addons