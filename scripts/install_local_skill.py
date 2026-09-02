#!/usr/bin/env python3
"""Install the standalone DZ Skill without exposing the nested plugin Skill twice."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SKILL_PARTS = (
    "SKILL.md",
    "agents",
    "assets",
    "references",
    "scripts",
    "schemas",
    "adapters",
    "portable",
    "hooks",
    "dz-manifest.json",
    "GETTING-STARTED.md",
    "LICENSE.md",
)
MARKER = ".dz-local-install.json"


class InstallError(RuntimeError):
    pass


def copy_ignore(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name == "__pycache__" or name == ".DS_Store" or name.endswith(".pyc")
    }


def read_workflow_version(source: Path) -> str:
    manifest = json.loads((source / "dz-manifest.json").read_text(encoding="utf-8"))
    version = manifest.get("workflow_version")
    if not isinstance(version, str) or not version.strip():
        raise InstallError("dz-manifest.json has no valid workflow_version")
    return version


def assert_source(source: Path) -> None:
    missing = [part for part in SKILL_PARTS if not (source / part).exists()]
    if missing:
        raise InstallError(f"DZ source is incomplete; missing: {', '.join(missing)}")


def managed_backup_path(target: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_root = target.parent.parent / "skill-backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    candidate = backup_root / f"{target.name}-{stamp}"
    suffix = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = backup_root / f"{target.name}-{stamp}-{suffix}"
        suffix += 1
    return candidate


def prepare_target(target: Path, replace: bool) -> Path | None:
    if not target.exists() and not target.is_symlink():
        return None
    if not replace:
        raise InstallError(
            f"Target already exists: {target}. Re-run with --replace after reviewing it."
        )
    if target.is_symlink():
        backup = managed_backup_path(target)
        target.replace(backup)
        return backup
    if not target.is_dir() or not (target / MARKER).is_file():
        raise InstallError(
            f"Refusing to replace an unmanaged path: {target}. Move it aside manually first."
        )
    backup = managed_backup_path(target)
    target.replace(backup)
    return backup


def install(source: Path, target: Path, replace: bool = False) -> tuple[Path, Path | None]:
    source = source.resolve()
    target = target.expanduser().absolute()
    assert_source(source)
    if target == source or source in target.parents:
        raise InstallError("Install target must be outside the DZ source repository")

    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".dz-installing-", dir=target.parent))
    backup: Path | None = None
    try:
        for part in SKILL_PARTS:
            src = source / part
            dst = staging / part
            if src.is_dir():
                shutil.copytree(src, dst, ignore=copy_ignore)
            else:
                shutil.copy2(src, dst)

        marker = {
            "name": "dz",
            "workflow_version": read_workflow_version(source),
            "installed_at": datetime.now(timezone.utc).isoformat(),
            "source": str(source),
            "layout": "standalone-single-entry",
        }
        (staging / MARKER).write_text(
            json.dumps(marker, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        skill_files = sorted(staging.rglob("SKILL.md"))
        if skill_files != [staging / "SKILL.md"]:
            raise InstallError("Standalone package must contain exactly one SKILL.md")

        backup = prepare_target(target, replace)
        staging.replace(target)
        return target, backup
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        if backup is not None and not target.exists():
            backup.replace(target)
        raise


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install one standalone DZ entry in the local Agent Skills directory."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.home() / ".agents" / "skills" / "dz",
        help="Install directory (default: ~/.agents/skills/dz)",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing symlink or previously managed DZ install",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = Path(__file__).resolve().parents[1]
    try:
        target, backup = install(source, args.target, args.replace)
    except (InstallError, OSError, json.JSONDecodeError) as exc:
        print(f"DZ install failed: {exc}", file=sys.stderr)
        return 1
    print(f"Installed one DZ Skill entry at: {target}")
    if backup is not None:
        print(f"Previous managed install saved at: {backup}")
    print("Restart the Agent host and open a new task to load the updated Skill.")
    print("After future source updates, run this installer again with --replace before restarting.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
