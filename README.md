![Static Badge](https://img.shields.io/badge/PYTHON-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square&logo=github&link=https%3A%2F%2Fgithub.com%2Fqaspen-python%2Fqaspen)
[![codecov](https://codecov.io/gh/chandr-andr/poetry-asterisk/graph/badge.svg?token=CT7FZVOR29)](https://codecov.io/gh/chandr-andr/poetry-asterisk)

# Poetry-Asterisk
This library performs auto change dependency version to `"*"`.
You can specify 3 parameters for detail setup.

# Installation
You can install this library this way:
```
poetry add poetry-asterisk
```
or with pip:
```
pip install poetry-asterisk
```


# Usage
Just run:
```
pasterisk
```

It has arguments:
- `exclude_packages`: specify what packages skip. Default: None
- `exclude_groups`: specify what groups skip (`dev`, `lint`, etc.). Default: None
- `path_to_pyproject`: path to the pyproject.toml. By default asterisk searches in the root directory.

Advanced example:
```
pasterisk --exclude_packages "pytest, orjson" --exclude_groups "lint" --path_to_pyproject ./pyproject.toml
```

# Example of work
`pyproject.toml` before update.
```toml
[tool.poetry]
name = "test"
version = "0.0.1"
description = ""
authors = ["awesome man"]
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.8.1,<4.0"
pydantic = "^2.4.2"

[tool.poetry.group.test.dependencies]
typing-extensions = "^4.8.0"
pytest = "^7.4.3"

[tool.poetry.group.lint.dependencies]
ruff = "^0.1.2"
```

command:
```
pasterisk --exclude_packages "pytest" --exclude_groups "lint"
```

`pyproject.toml` after update. We didn't touched `pytest` and the whole `lint` group
```toml
[tool.poetry]
name = "test"
version = "0.0.1"
description = ""
authors = ["awesome man"]
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.8.1,<4.0"
pydantic = "*"

[tool.poetry.group.test.dependencies]
typing-extensions = "*"
pytest = "^7.4.3"

[tool.poetry.group.lint.dependencies]
ruff = "^0.1.2"
```
