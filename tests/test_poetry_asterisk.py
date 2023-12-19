from __future__ import annotations

from pathlib import Path

from tomlkit import parse

from poetry_asterisk.poetry_asterisk import PoetryAsteriskProcessor


def test_change_dependencies(
    test_pyproject_file: str,
) -> None:
    """Test change main pyproject dependencies."""
    pap = PoetryAsteriskProcessor(
        exclude_packages={"pytest", "pydantic"},
        exclude_groups={"lint"},
        path_to_pyproject=test_pyproject_file,
    )

    pap.process_pyproject()

    with Path(test_pyproject_file).open() as pyproject_file:
        parsed_toml_file = parse(string=pyproject_file.read())

    main_deps = parsed_toml_file["tool"]["poetry"][  # type: ignore[index]
        "dependencies"
    ]

    assert main_deps["python"] == ">=3.8.1,<4.0"  # type: ignore[index]
    assert main_deps["tomlkit"] == {"version": "*", "optional": True}  # type: ignore[index]
    assert main_deps["pydantic"] == "^0.1.2"  # type: ignore[index]

    test_deps = parsed_toml_file["tool"]["poetry"]["group"]["test"][  # type: ignore[index]
        "dependencies"
    ]

    assert test_deps["pytest"] == "^7.4.3"  # type: ignore[index]
    assert test_deps["pre-commit"] == "*"  # type: ignore[index]
    assert test_deps["anyio"] == "*"  # type: ignore[index]

    lint_deps = parsed_toml_file["tool"]["poetry"]["group"]["lint"][  # type: ignore[index]
        "dependencies"
    ]

    assert lint_deps["ruff"] == "^0.1.2"  # type: ignore[index]
    assert lint_deps["isort"] == "^0.1.2"  # type: ignore[index]
