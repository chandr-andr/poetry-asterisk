"""Main entrypoint to application."""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from poetry_asterisk.poetry_asterisk import PoetryAsteriskProcessor


def main() -> None:
    """Run main application."""
    arg_parser = ArgumentParser(
        prog="Poetry Asterisk",
        description="Change dependencies version to asterisk.",
    )

    arg_parser.add_argument(
        "-e",
        "--exclude_packages",
        type=str,
        required=False,
        help="""USAGE: --exclude_packages "pytest,ruff"  !without spaces""",
    )

    arg_parser.add_argument(
        "-p",
        "--path_to_pyproject",
        type=Path,
        required=False,
        help="USAGE: --path_to_pyproject ./pyproject.toml",
    )

    arg_parser.add_argument(
        "-g",
        "--exclude_groups",
        type=str,
        required=False,
        help="""USAGE: --exclude_groups "dev,link"  !without spaces""",
    )

    parsed_args = arg_parser.parse_args()
    exclude_packages: set[str] | None = (
        set(parsed_args.exclude_packages.split(","))
        if parsed_args.exclude_packages
        else None
    )
    exclude_groups: set[str] | None = (
        set(parsed_args.exclude_groups.split(","))
        if parsed_args.exclude_groups
        else None
    )
    path_to_pyproject: str | None = parsed_args.path_to_pyproject

    PoetryAsteriskProcessor(
        exclude_packages=exclude_packages,
        exclude_groups=exclude_groups,
        path_to_pyproject=path_to_pyproject,
    ).process_pyproject()


if __name__ == "__main__":
    main()
