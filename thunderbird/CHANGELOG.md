<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.0.0

- Initial Thunderbird add-on, based on jlesage/docker-thunderbird v26.07.1 (Thunderbird 151.0.1-r0).
- Persists the Thunderbird profile (mail accounts, local folders, settings) to `/data` and
  provides a `downloads` folder mapped to `/share/thunderbird` for saving attachments, so
  everything survives add-on updates and restarts.
- Runs Thunderbird as an unprivileged user (no extra capabilities needed).
- Ships a hardened AppArmor profile (capabilities scoped to what the init system and
  Thunderbird need, plus mount and ptrace rules) instead of running unconfined.
