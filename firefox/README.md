# Home Assistant Add-on: Firefox

_Run Firefox as a browser inside Home Assistant to access local or external web sites from your home._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

## About

Mozilla Firefox is a free and open-source web browser developed by Mozilla Foundation and its subsidiary, Mozilla Corporation.

This add-on is based on the [docker image](https://github.com/jlesage/docker-firefox) from [Jocelyn Le Sage](https://github.com/jlesage).

A huge thank to him for the great containers created and maintained.
He's the real hero who needs to be [supported](https://github.com/sponsors/jlesage).

## Differences with the original container

There are a few differences that were either required for this container to work as an Add-on or just my own tweaks based on my preferences:

- This container is not based on Alpine **Stable** but Alpine **Edge**. The main reason was to benefit from the latest Firefox version available. During the startup, the container may show in the log an older version of Firefox, it can be ignored.
- To make it compatible with Home Assistant persistence, I needed to remap folders and to do so, the startup script runs as `root`. I will try to avoid this in the future.

## How to use

Just install, start the container and click on "Open Web UI". You can use "Show in sidebar" for easy access. Everything you do is persisted in Firefox. Even if you stop the Add-on or restart Home Assistant host OS.

## Downloads

The files downloaded in Firefox are automatically stored to your `/share/firefox` folder.

## Import bookmarks

You can import `bookmarks.html` file by dropping them in your `/share/firefox` folder and import the `bookmarks.html` file in Firefox.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
