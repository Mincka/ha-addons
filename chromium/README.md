# Home Assistant Add-on: Chromium

_Run Chromium as a browser inside Home Assistant to access local or external web sites from your home._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

## About

Chromium is a free and open-source web browser project, primarily developed and maintained by Google. It is the open-source codebase that Google Chrome and many other browsers are built upon.

This add-on is based on the [docker image](https://github.com/jlesage/docker-chromium) from [Jocelyn Le Sage](https://github.com/jlesage).

A huge thank to him for the great containers created and maintained.
He's the real hero who needs to be [supported](https://github.com/sponsors/jlesage).

## Difference with the original container

To make it compatible with Home Assistant persistence, the Chromium profile is remapped to the add-on's `/data` volume and downloads to the `/share/chromium` folder. This remapping happens during container initialization, so Chromium itself runs as an unprivileged user with its sandbox enabled.

## How to use

Just install, start the container and click on "Open Web UI". You can use "Show in sidebar" for easy access. Everything you do is persisted in Chromium, even if you stop the add-on or restart the Home Assistant host.

## File browser and terminal

The underlying image includes an integrated web file manager and a web terminal. Both are disabled by default and can be enabled from the add-on's Configuration tab (`WEB_FILE_MANAGER` and `WEB_TERMINAL`).

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
