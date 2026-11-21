# Home Assistant Add-on: Thunderbird

_Run Thunderbird as an email client inside Home Assistant to access your mailboxes from your home._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

## About

Thunderbird is a free and open-source email, calendar and chat client developed by MZLA Technologies Corporation, a subsidiary of the Mozilla Foundation.

This add-on is based on the [docker image](https://github.com/jlesage/docker-thunderbird) from [Jocelyn Le Sage](https://github.com/jlesage).

A huge thank to him for the great containers created and maintained.
He's the real hero who needs to be [supported](https://github.com/sponsors/jlesage).

## Difference with the original container

To make it compatible with Home Assistant persistence, the Thunderbird profile (mail accounts, local folders, settings) is remapped to the add-on's `/data` volume, and a `downloads` folder pointing to `/share/thunderbird` is provided for saving attachments. This remapping happens during container initialization, so Thunderbird itself runs as an unprivileged user.

## How to use

Just install, start the container and click on "Open Web UI". You can use "Show in sidebar" for easy access. Everything you do is persisted in Thunderbird, even if you stop the add-on or restart the Home Assistant host.

To save attachments where other add-ons and the host can reach them, use the `downloads` folder (it maps to `/share/thunderbird`).

## File browser and terminal

The underlying image includes an integrated web file manager and a web terminal. Both are disabled by default and can be enabled from the add-on's Configuration tab (`WEB_FILE_MANAGER` and `WEB_TERMINAL`).

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
