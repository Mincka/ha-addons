#!/usr/bin/env python3
"""Deterministic helpers for the upstream sync workflow.

Everything that must look the same across add-ons (Dockerfile tag, tracked
version file, version bump, CHANGELOG entry, PR body) is produced here, so
the PRs for Firefox, Chromium and Thunderbird all follow one format. The
Claude step of the workflow only adds new options (config.yaml and
translations), and `apply` checks that it stayed within that scope.

Subcommands:
  known-options  List options that other add-ons (on the current branch and
                 on open update branches) define but the target add-on lacks,
                 so a new option gets the same default and wording everywhere.
  apply          Validate the option changes, then update Dockerfile(s),
                 version file, config.yaml version(s) and CHANGELOG(s), and
                 write the PR body.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import textwrap
from pathlib import Path

WRAP = 80
ADDONS = ("firefox", "firefox_edge", "chromium", "thunderbird")
KEY_RE = re.compile(r"^  ([A-Z][A-Z0-9_]*):(.*)$")


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------

def run(*args: str, check: bool = True) -> str:
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode != 0:
        sys.exit(f"command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout


def git_show(ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"], capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout if result.returncode == 0 else None


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    # newline="\n" keeps LF endings when this runs on Windows too.
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def fail(message: str) -> None:
    sys.exit(f"::error::{message}")


# --------------------------------------------------------------------------
# config.yaml / translations parsing (line based, no PyYAML dependency)
# --------------------------------------------------------------------------

def block_entries(text: str, block: str) -> dict[str, str]:
    """Return {KEY: raw value} for the 2-space-indented keys of a top-level block."""
    entries: dict[str, str] = {}
    inside = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            inside = line.rstrip() == f"{block}:"
            continue
        if inside:
            m = KEY_RE.match(line)
            if m:
                entries[m.group(1)] = m.group(2).strip()
    return entries


def parse_translations(text: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    current = None
    inside = False
    for line in text.splitlines():
        if not line.strip():
            continue
        if not line.startswith(" "):
            inside = line.rstrip() == "configuration:"
            current = None
            continue
        if not inside:
            continue
        m = KEY_RE.match(line)
        if m:
            current = m.group(1)
            result[current] = {}
            continue
        m = re.match(r"^    (name|description):\s*(.*)$", line)
        if m and current:
            result[current][m.group(1)] = m.group(2).strip()
    return result


def config_version(text: str) -> str:
    m = re.search(r'^version:\s*"?(\d+\.\d+\.\d+)"?\s*$', text, re.M)
    if not m:
        fail("could not find the version field in config.yaml")
    return m.group(1)


def bump(version: str, kind: str) -> str:
    major, minor, patch = (int(x) for x in version.split("."))
    return f"{major}.{minor + 1}.0" if kind == "minor" else f"{major}.{minor}.{patch + 1}"


# --------------------------------------------------------------------------
# Upstream releases
# --------------------------------------------------------------------------

def fetch_releases(repo: str, tracked: str, latest: str) -> list[dict]:
    """Releases newer than `tracked` up to and including `latest`, newest first."""
    data = json.loads(run("gh", "api", f"repos/{repo}/releases?per_page=100"))
    releases = [r for r in data if not r.get("draft") and not r.get("prerelease")]
    tags = [r["tag_name"] for r in releases]
    if latest not in tags:
        fail(f"{latest} not found in {repo} releases")
    start = tags.index(latest)
    end = tags.index(tracked) if tracked in tags else start + 1
    if tracked not in tags:
        print(f"::warning::tracked version {tracked} not found upstream; using {latest} only")
    return releases[start:end]


def parse_body(body: str) -> list[tuple[int, str]]:
    """Turn a release body into (depth, text) bullets, depth starting at 0."""
    items: list[tuple[int, str]] = []
    for raw in (body or "").replace("\r", "").splitlines():
        if not raw.strip() or raw.strip().lower().startswith("changes in this release"):
            continue
        m = re.match(r"^(\s*)[-*] (.*)$", raw)
        if m:
            items.append((len(m.group(1)) // 2, m.group(2).strip()))
        elif items:  # continuation of the previous bullet
            depth, text = items[-1]
            items[-1] = (depth, f"{text} {raw.strip()}")
    if not items:
        return []
    base = min(d for d, _ in items)
    normalized = []
    for depth, text in items:
        text = re.sub(r",\s*(which brings|bringing) the following changes:$", ":", text)
        normalized.append((depth - base, text))
    return normalized


def is_app_update(items: list[tuple[int, str]]) -> bool:
    """True when a release updates the application itself (not only the baseimage)."""
    return any(
        depth == 0 and re.match(r"^Updated (?!baseimage\b)\S+ to version ", text)
        for depth, text in items
    )


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def bullet(depth: int, text: str) -> list[str]:
    indent = "  " * depth
    return textwrap.wrap(
        text,
        width=WRAP,
        initial_indent=f"{indent}- ",
        subsequent_indent=f"{indent}  ",
        break_long_words=False,
        break_on_hyphens=False,
    ) or [f"{indent}-"]


def first_sentence(text: str) -> str:
    m = re.match(r"^(.+?\.)(\s|$)", text)
    return m.group(1) if m else text


def changelog_entry(version: str, repo: str, latest: str, releases: list[dict],
                    new_options: list[str], translations: dict) -> str:
    lines = [f"## {version}", "", f"- Base image update: {repo} to {latest}"]
    if len(releases) == 1:
        for depth, text in parse_body(releases[0]["body"]):
            lines += bullet(depth + 1, text)
    else:
        for release in releases:
            lines += bullet(1, f"{release['tag_name']}:")
            for depth, text in parse_body(release["body"]):
                lines += bullet(depth + 2, text)
    if new_options:
        noun = "variable" if len(new_options) == 1 else "variables"
        lines.append(f"- Added new environment {noun}:")
        for key in new_options:
            summary = first_sentence(translations.get(key, {}).get("description", ""))
            lines += bullet(1, f"{key}: {summary}" if summary else key)
    return "\n".join(lines) + "\n"


def insert_changelog(path: str, entry: str) -> None:
    text = read(path)
    m = re.search(r"^## ", text, re.M)
    if m:
        text = text[: m.start()] + entry + "\n" + text[m.start():]
    else:
        text = text.rstrip("\n") + "\n\n" + entry
    write(path, text)


# --------------------------------------------------------------------------
# Subcommands
# --------------------------------------------------------------------------

def cmd_known_options(args: argparse.Namespace) -> None:
    """Print, as Markdown, the options of other add-ons missing from the target."""
    target_opts = set(block_entries(read(f"{args.addon}/config.yaml"), "options"))
    refs = ["HEAD"] + [
        r for r in run("git", "for-each-ref", "--format=%(refname:short)",
                       "refs/remotes/origin/update-upstream-*").split()
    ]
    seen: dict[str, dict] = {}
    for ref in refs:
        for addon in ADDONS:
            if addon == args.addon:
                continue
            config = git_show(ref, f"{addon}/config.yaml")
            trans = git_show(ref, f"{addon}/translations/en.yaml")
            if not config or not trans:
                continue
            options = block_entries(config, "options")
            schema = block_entries(config, "schema")
            texts = parse_translations(trans)
            for key, default in options.items():
                if key in target_opts or key in seen:
                    continue
                seen[key] = {
                    "source": f"{addon} ({'main' if ref == 'HEAD' else ref})",
                    "default": default,
                    "schema": schema.get(key, "str"),
                    **texts.get(key, {}),
                }
    if not seen:
        print("_No option defined elsewhere is missing from this add-on._")
        return
    for key, info in seen.items():
        print(f"- `{key}` (from {info['source']})")
        print(f"  - options: `{key}: {info['default']}` / schema: `{key}: {info['schema']}`")
        print(f"  - name: `{info.get('name', '')}`")
        print(f"  - description: `{info.get('description', '')}`")


def cmd_apply(args: argparse.Namespace) -> None:
    folders = [args.addon] + [f for f in args.extra if f]
    allowed = set()
    for folder in folders:
        allowed.add(f"{folder}/config.yaml")
        allowed.update(str(p).replace("\\", "/") for p in Path(folder, "translations").glob("*.yaml"))

    # 1. The Claude step must not have committed or touched other files.
    if run("git", "rev-parse", "HEAD").strip() != args.base_sha:
        fail("HEAD moved during the Claude step: it must not commit")
    changed = [l[3:] for l in run("git", "status", "--porcelain", "--untracked-files=all").splitlines()]
    stray = [p for p in changed if p not in allowed]
    if stray:
        fail(f"files changed outside the allowed scope: {', '.join(stray)}")

    # 2. Collect and validate new options per folder.
    new_by_folder: dict[str, list[str]] = {}
    translations_by_folder: dict[str, dict] = {}
    for folder in folders:
        base_cfg = git_show("HEAD", f"{folder}/config.yaml") or ""
        cfg = read(f"{folder}/config.yaml")
        if config_version(cfg) != config_version(base_cfg):
            fail(f"{folder}/config.yaml version must not be changed by the Claude step")
        before, after = block_entries(base_cfg, "options"), block_entries(cfg, "options")
        removed = sorted(set(before) - set(after))
        if removed:
            fail(f"{folder}: options removed: {', '.join(removed)}")
        new = [k for k in after if k not in before]
        schema = block_entries(cfg, "schema")
        texts = parse_translations(read(f"{folder}/translations/en.yaml"))
        for key in new:
            if key not in schema:
                fail(f"{folder}: new option {key} is missing from schema")
            if not texts.get(key, {}).get("name") or not texts.get(key, {}).get("description"):
                fail(f"{folder}: new option {key} needs a name and description in translations/en.yaml")
        new_by_folder[folder] = new
        translations_by_folder[folder] = texts
    if len({tuple(sorted(v)) for v in new_by_folder.values()}) > 1:
        fail(f"new options differ between {', '.join(folders)}: {new_by_folder}")

    # 3. Upstream releases and bump kind.
    releases = fetch_releases(args.repo, args.tracked, args.latest)
    app_update = any(is_app_update(parse_body(r["body"])) for r in releases)
    new_options = new_by_folder[args.addon]
    kind = "minor" if new_options or app_update else "patch"
    reason = (
        "new options" if new_options else f"{args.app} update" if app_update else "baseimage-only update"
    )
    if new_options and app_update:
        reason = f"new options and {args.app} update"

    image = args.repo.split("/")[0] + "/" + args.repo.split("/")[1].removeprefix("docker-")
    bumps = []
    for folder in folders:
        # Dockerfile
        dockerfile = f"{folder}/Dockerfile"
        text, count = re.subn(rf"^FROM {re.escape(image)}:\S+", f"FROM {image}:{args.latest}",
                              read(dockerfile), count=1, flags=re.M)
        if count != 1:
            fail(f"{dockerfile}: no 'FROM {image}:<tag>' line")
        write(dockerfile, text)

        # config.yaml version
        cfg = read(f"{folder}/config.yaml")
        old = config_version(cfg)
        new = bump(old, kind)
        cfg = re.sub(r'^version:.*$', f'version: "{new}"', cfg, count=1, flags=re.M)
        write(f"{folder}/config.yaml", cfg)
        bumps.append((folder, old, new))

        # CHANGELOG
        insert_changelog(
            f"{folder}/CHANGELOG.md",
            changelog_entry(new, args.repo, args.latest, releases, new_options,
                            translations_by_folder[folder]),
        )

    # Tracked version file, always with a trailing newline.
    write(args.version_file, f"{args.latest}\n")

    # 4. PR body.
    url = f"https://github.com/{args.repo}"
    body = [
        "## Automated upstream sync",
        "",
        f"**Upstream:** [{args.repo}]({url}) `{args.tracked}` → "
        f"[`{args.latest}`]({url}/releases/tag/{args.latest})",
        "",
        "### Upstream releases included",
        "",
        *[f"- [`{r['tag_name']}`]({r['html_url']})" for r in releases],
        "",
        f"### Add-on version ({kind}: {reason})",
        "",
        "| Add-on | Version |",
        "| --- | --- |",
        *[f"| `{f}` | `{o}` → `{n}` |" for f, o, n in bumps],
        "",
        "### New options",
        "",
    ]
    if new_options:
        texts = translations_by_folder[args.addon]
        defaults = block_entries(read(f"{args.addon}/config.yaml"), "options")
        for key in new_options:
            body.append(f"- `{key}` (default `{defaults[key]}`): {texts[key]['description']}")
    else:
        body.append("_None._")
    body += [
        "",
        "### Checklist",
        "",
        f"- [ ] Review the CHANGELOG entr{'ies' if len(folders) > 1 else 'y'} "
        f"in {', '.join(f'`{f}/`' for f in folders)}",
        "- [ ] Check the default value and wording of new options (if any)",
        "- [ ] Test the add-on after the image build",
        "",
        "---",
        "*Created automatically by the upstream sync workflow "
        "(Claude Code adds new options; the rest is generated by `.github/scripts/upstream_sync.py`).*",
    ]
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write(str(out / "pr-body.md"), "\n".join(body) + "\n")
    print("\n".join(body))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("known-options")
    p.add_argument("--addon", required=True)
    p.set_defaults(func=cmd_known_options)

    p = sub.add_parser("apply")
    p.add_argument("--addon", required=True)
    p.add_argument("--extra", action="append", default=[])
    p.add_argument("--app", required=True, help="Application name, e.g. Firefox")
    p.add_argument("--repo", required=True, help="Upstream repo, e.g. jlesage/docker-firefox")
    p.add_argument("--tracked", required=True)
    p.add_argument("--latest", required=True)
    p.add_argument("--version-file", required=True)
    p.add_argument("--base-sha", required=True)
    p.add_argument("--out-dir", required=True)
    p.set_defaults(func=cmd_apply)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
