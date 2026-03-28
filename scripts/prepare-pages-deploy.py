#!/usr/bin/env python3
"""
Prepare a minimal Cloudflare Pages bundle in dist/pages.

Only runtime assets required by the static site are copied so repository
internals never become public by accident.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_ROOT = (REPO_ROOT / "dist").resolve()
DEFAULT_OUTPUT_DIR = DIST_ROOT / "pages"
REQUIRED_PUBLIC_PATHS = (
    "index.html",
    "_headers",
    "assets",
    "data",
)
OPTIONAL_PUBLIC_PATHS = (
    "_redirects",
    "favicon.ico",
    "robots.txt",
    "sitemap.xml",
)


def resolve_output_dir(raw_output: str) -> Path:
    output_dir = Path(raw_output)
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir
    output_dir = output_dir.resolve()

    try:
        output_dir.relative_to(DIST_ROOT)
    except ValueError as exc:
        raise SystemExit(
            f"Output path must stay inside {DIST_ROOT} for safe deployment packaging."
        ) from exc

    if output_dir == DIST_ROOT:
        raise SystemExit("Output path must be a subdirectory inside dist/, not dist/ itself.")

    return output_dir


def ensure_safe_output_dir(output_dir: Path) -> None:
    for relative_path in REQUIRED_PUBLIC_PATHS + OPTIONAL_PUBLIC_PATHS:
        source_path = (REPO_ROOT / relative_path).resolve()
        if not source_path.exists():
            continue

        try:
            output_dir.relative_to(source_path)
        except ValueError:
            continue

        raise SystemExit(
            f"Output path {output_dir} cannot be inside source path {source_path}."
        )


def reset_output_dir(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


def copy_path(source_path: Path, output_dir: Path) -> int:
    destination_path = output_dir / source_path.name
    if source_path.is_dir():
        shutil.copytree(source_path, destination_path)
        return sum(1 for child in destination_path.rglob("*") if child.is_file())

    shutil.copy2(source_path, destination_path)
    return 1


def prepare_bundle(output_dir: Path) -> tuple[list[str], int]:
    copied_items: list[str] = []
    copied_files = 0

    for relative_path in REQUIRED_PUBLIC_PATHS:
        source_path = REPO_ROOT / relative_path
        if not source_path.exists():
            raise SystemExit(f"Required public path is missing: {source_path}")
        copied_files += copy_path(source_path, output_dir)
        copied_items.append(relative_path)

    for relative_path in OPTIONAL_PUBLIC_PATHS:
        source_path = REPO_ROOT / relative_path
        if not source_path.exists():
            continue
        copied_files += copy_path(source_path, output_dir)
        copied_items.append(relative_path)

    return copied_items, copied_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare the safe Cloudflare Pages deployment bundle.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Bundle output directory. Must stay inside dist/.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    output_dir = resolve_output_dir(args.output)
    ensure_safe_output_dir(output_dir)
    reset_output_dir(output_dir)
    copied_items, copied_files = prepare_bundle(output_dir)

    print(f"Prepared Cloudflare Pages bundle at: {output_dir}")
    print(f"Copied {copied_files} files from {len(copied_items)} public paths:")
    for relative_path in copied_items:
        print(f"  - {relative_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
