<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.0.0

- Initial Chromium add-on, based on jlesage/docker-chromium v26.07.1 (Chromium 149.0.7827.200-r0).
- Persists the Chromium profile to `/data` and stores downloads in `/share/chromium` so they
  survive add-on updates and restarts.
- Runs Chromium with its sandbox enabled (via the `SYS_ADMIN` capability), avoiding the
  `--no-sandbox` fallback and its "unsupported command-line flag" infobar.
- Ships a Home Assistant-tolerant tmp-clear init script so the add-on starts cleanly under the
  supervisor's `/tmp/run` bind-mounts.
- Ships a hardened AppArmor profile (scoped capabilities, mount and ptrace rules) instead of
  running unconfined. Note: because it restricts writes to system directories, enabling
  `INSTALL_PACKAGES` or `ENABLE_CJK_FONT` (which run `apk` at startup) is not compatible with the
  profile; disable AppArmor (`apparmor: false`) if you need those.
