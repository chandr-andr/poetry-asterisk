from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Final, MutableMapping

from tomlkit import TOMLDocument, dumps, parse

if TYPE_CHECKING:
    from tomlkit.items import InlineTable
    from typing_extensions import Self


class PoetryAsteriskProcessor:
    """Class to process `pyproject.toml` file.

    Change dependencies versions to `"*"` if dependency isn't
    in `exclude_packages`.
    """

    def __init__(
        self: Self,
        exclude_packages: set[str] | None = None,
        exclude_groups: set[str] | None = None,
        path_to_pyproject: str | None = None,
    ) -> None:
        """Create new instance of `PoetryAsteriskProcessor`.

        ### Parameters:
        - `exclude_packages`: packages to exclude from processing.
        - `path_to_pyproject`: path to `pyproject.toml`.
        """
        self.path_to_pyproject: Final = (
            path_to_pyproject or str(Path.cwd()) + "/pyproject.toml"
        )

        if exclude_packages:
            exclude_packages.add("python")

        self.exclude_packages: Final = set(exclude_packages or ["python"])
        self.exclude_groups: Final = set(exclude_groups or [])

    def process_pyproject(self: Self) -> None:
        """Process `pyproject.toml`.

        Read `pyproject.toml` file and parse it into `TOMLDocument`
        instance.

        Process dependencies in the file and then save new version
        of toml data.
        """
        with Path(self.path_to_pyproject).open() as pyproject_file:
            parsed_toml_file = parse(string=pyproject_file.read())

        parsed_toml_file = self._process_pyproject(
            parsed_toml_file=parsed_toml_file,
        )

        with Path(self.path_to_pyproject).open("w") as pyproject_file:
            pyproject_file.write(dumps(parsed_toml_file))

    def _process_pyproject(
        self: Self,
        parsed_toml_file: TOMLDocument,
    ) -> TOMLDocument:
        parsed_toml_file = self._process_main_dependencies(
            parsed_toml_file=parsed_toml_file,
        )
        return self._process_group_dependencies(
            parsed_toml_file=parsed_toml_file,
        )

    def _process_main_dependencies(
        self: Self,
        parsed_toml_file: TOMLDocument,
    ) -> TOMLDocument:
        dependencies: InlineTable = parsed_toml_file[
            "tool"
        ][  # type: ignore[index, assignment]
            "poetry"
        ][
            "dependencies"
        ]

        self._process_dependencies(
            dependencies=dependencies,
        )

        return parsed_toml_file

    def _process_group_dependencies(
        self: Self,
        parsed_toml_file: TOMLDocument,
    ) -> TOMLDocument:
        dependencies_groups: InlineTable = parsed_toml_file[
            "tool"
        ][  # type: ignore[index, assignment]
            "poetry"
        ][
            "group"
        ]

        for dependency_group in dependencies_groups:
            if dependency_group in self.exclude_groups:
                continue

            dependencies: InlineTable = dependencies_groups[
                dependency_group
            ][  # type: ignore[index]
                "dependencies"
            ]
            self._process_dependencies(
                dependencies=dependencies,
            )

        return parsed_toml_file

    def _process_dependencies(
        self: Self,
        dependencies: InlineTable,
    ) -> InlineTable:
        for dependency_name in dependencies:
            if dependency_name == "*":
                continue

            if dependency_name in self.exclude_packages:
                continue

            if isinstance(dependencies[dependency_name], str):
                dependencies[dependency_name] = "*"
            elif isinstance(dependencies[dependency_name], MutableMapping):
                dependencies[dependency_name][
                    "version"
                ] = "*"  # type: ignore[index]

        return dependencies
