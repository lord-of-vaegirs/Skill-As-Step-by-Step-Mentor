#!/usr/bin/env python3
"""Create, inspect, copy, list, and delete mentor progress Markdown files."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

PROGRESS_MARKER = "schema_version: 1"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        slug = "learning"
    return slug[:48].rstrip("-")


def resolve_root(raw: str) -> Path:
    root = Path(raw).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    return root


def resolve_inside(root: Path, raw: str, *, must_exist: bool = False) -> Path:
    candidate = Path(raw).expanduser()
    path = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes root {root}: {path}") from exc
    if must_exist and not path.is_file():
        raise ValueError(f"Progress file not found: {path}")
    return path


def quote_yaml(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def progress_document(args: argparse.Namespace) -> str:
    timestamp = now_iso()
    sources = args.sources.strip() or "None provided."
    return f'''---
schema_version: 1
session_id: {quote_yaml(str(uuid.uuid4()))}
topic: {quote_yaml(args.topic)}
goal: {quote_yaml(args.goal)}
foundation: {quote_yaml(args.foundation)}
status: "active"
current_checkpoint: "diagnostic"
created_at: {quote_yaml(timestamp)}
updated_at: {quote_yaml(timestamp)}
---

# Learning Progress: {args.topic}

## Sources

- {sources}

## Route

- [ ] Diagnostic — establish prerequisites
- [ ] Route design — adapt chapters from diagnostic evidence
- [ ] Integration — verify the final artifact against the goal

## Current checkpoint

**ID:** diagnostic

**Next action:** Complete a short prerequisite diagnostic.

## Evidence

- No evidence recorded yet.

## Open questions

- None.

## History

- {timestamp} — Session created.
'''


def validate_progress(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or PROGRESS_MARKER not in text[:500]:
        raise ValueError(f"Not a mentor progress file: {path}")


def cmd_init(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    filename = args.filename or f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{slugify(args.topic)}.md"
    path = resolve_inside(root, filename)
    if path.exists() and not args.force:
        raise ValueError(f"Refusing to overwrite existing file: {path}")
    atomic_write(path, progress_document(args))
    print(path)
    return 0


def progress_files(root: Path) -> list[Path]:
    found: list[Path] = []
    for path in sorted(root.glob("*.md")):
        try:
            validate_progress(path)
        except (OSError, UnicodeError, ValueError):
            continue
        found.append(path)
    return found


def cmd_list(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    files = progress_files(root)
    for path in files:
        print(path)
    if not files:
        print(f"No progress files found under {root}", file=sys.stderr)
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    path = resolve_inside(root, args.file, must_exist=True)
    validate_progress(path)
    sys.stdout.write(path.read_text(encoding="utf-8"))
    return 0


def cmd_copy(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    source = resolve_inside(root, args.file, must_exist=True)
    validate_progress(source)
    destination = resolve_inside(root, args.destination)
    if destination.exists() and not args.force:
        raise ValueError(f"Refusing to overwrite existing file: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=f".{destination.name}.", delete=False) as handle:
        temp = Path(handle.name)
    try:
        shutil.copyfile(source, temp)
        os.replace(temp, destination)
    finally:
        temp.unlink(missing_ok=True)
    print(destination)
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    root = resolve_root(args.root)
    path = resolve_inside(root, args.file, must_exist=True)
    validate_progress(path)
    if not args.yes:
        print(f"Would delete: {path}")
        print("Re-run with --yes to confirm.")
        return 2
    path.unlink()
    print(f"Deleted: {path}")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--root", default=".", help="Authorized progress directory (default: current directory)")
    sub = result.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a progress Markdown file")
    init.add_argument("--topic", required=True)
    init.add_argument("--goal", required=True)
    init.add_argument("--foundation", default="Not provided.")
    init.add_argument("--sources", default="")
    init.add_argument("--filename")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=cmd_init)

    listing = sub.add_parser("list", help="List valid progress files")
    listing.set_defaults(func=cmd_list)

    show = sub.add_parser("show", help="Print a validated progress file")
    show.add_argument("file")
    show.set_defaults(func=cmd_show)

    copy = sub.add_parser("copy", help="Atomically copy a progress file within root")
    copy.add_argument("file")
    copy.add_argument("destination")
    copy.add_argument("--force", action="store_true")
    copy.set_defaults(func=cmd_copy)

    delete = sub.add_parser("delete", help="Preview or confirm deletion of one progress file")
    delete.add_argument("file")
    delete.add_argument("--yes", action="store_true", help="Confirm deletion")
    delete.set_defaults(func=cmd_delete)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
