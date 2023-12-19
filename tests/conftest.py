"""Main conftest for all tests."""
from __future__ import annotations

import asyncio
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Generator

import pytest
from tomlkit import dumps

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy(),
    )


@pytest.fixture()
def test_pyproject_file_name() -> str:
    """Random name for the file with toml file."""
    return uuid.uuid4().hex


@pytest.fixture()
def test_pyproject_data() -> dict[str, Any]:
    """Test pyproject data."""
    return {
        "tool": {
            "poetry": {
                "name": "poetry-asterisk",
                "version": "0.1.0",
                "description": "",
                "authors": [
                    "chandr-andr (Kiselev Aleksandr) <askiselev00@gmail.com>",
                ],
                "readme": "README.md",
                "packages": [
                    {"include": "poetry_asterisk"},
                ],
                "dependencies": {
                    "python": ">=3.8.1,<4.0",
                    "tomlkit": {"version": "^0.1.2", "optional": True},
                    "pydantic": "^0.1.2",
                },
                "group": {
                    "test": {
                        "dependencies": {
                            "pytest": "^7.4.3",
                            "pre-commit": "*",
                            "anyio": "^0.1.2",
                        },
                    },
                    "lint": {
                        "dependencies": {
                            "ruff": "^0.1.2",
                            "isort": "^0.1.2",
                        },
                    },
                },
            },
        },
        "build-system": {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api",
        },
    }


@pytest.fixture()
def test_pyproject_file(
    test_pyproject_file_name: str,
    test_pyproject_data: dict[str, Any],
) -> Generator[str, None, None]:
    """Create test pyproject file.

    Return path to the file.
    """
    path = f"./{test_pyproject_file_name}"
    with Path(path).open("w") as file:
        file.write(dumps(test_pyproject_data))
    yield path
    os.remove(path)  # noqa: PTH107
