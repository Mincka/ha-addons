# Home Assistant Add-on: Firefox

_Run Firefox as a browser inside Home Assistant to access local or external web sites from your home._

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

## About

Mozilla Firefox is a free and open-source web browser developed by Mozilla Foundation and its subsidiary, Mozilla Corporation.

This add-on is based on the [docker image](https://github.com/jlesage/docker-firefox) from [Jocelyn Le Sage](https://github.com/jlesage).

A huge thank to him for the great containers created and maintained.
He's the real hero who needs to be [supported](https://github.com/sponsors/jlesage).

## Difference with the original container

To make it compatible with Home Assistant persistence, the Firefox profile is remapped to the add-on's `/data` volume and downloads to the `/share/firefox` folder. This remapping happens during container initialization, so Firefox itself runs as an unprivileged user.

## How to use

Just install, start the container and click on "Open Web UI". You can use "Show in sidebar" for easy access. Everything you do is persisted in Firefox, even if you stop the Add-on or restart Home Assistant host OS.

## File browser and terminal

The underlying image includes an integrated web file manager and a web terminal. Both are disabled by default and can be enabled from the add-on's Configuration tab (`WEB_FILE_MANAGER` and `WEB_TERMINAL`).

## Downloads

The files downloaded in Firefox are automatically stored to your `/share/firefox` folder.

## Uploads

If you need to upload files through the Firefox add-on, you can use the [File editor add-on](https://github.com/home-assistant/addons/blob/master/configurator/) to upload the files to your `/share/firefox` folder.
The files will be available in the `downloads` folder of the add-on. You can browse to this location when you select the files to upload.

## Import bookmarks

You can import `bookmarks.html` file by dropping them in your `/share/firefox` folder and import the `bookmarks.html` file in Firefox.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
