"""Exercise the installed console entry point with local schemas."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def schema_path(tmp_path: Path) -> Path:
    path = tmp_path / "schema.json"
    path.write_text(
        json.dumps(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": False,
            }
        ),
        encoding="utf-8",
    )
    return path


def run_cli(*args: str, env=None) -> subprocess.CompletedProcess:
    command = Path(sys.executable).with_name("check-json-schema-meta")
    return subprocess.run(
        [str(command), *args], capture_output=True, text=True, env=env, check=False
    )


@pytest.mark.parametrize(
    ("case", "args", "expected"),
    [
        ("valid", [], 0),
        ("invalid-value", [], 1),
        ("missing-schema", [], 0),
        ("missing-schema", ["--strict"], 1),
        ("array", [], 0),
        ("array", ["--strict"], 1),
        ("invalid-json", [], 1),
        ("missing-file", [], 1),
        ("missing-reference", [], 1),
    ],
)
def test_installed_cli(
    tmp_path: Path, schema_path: Path, case: str, args: list, expected: int
) -> None:
    path = tmp_path / "input.json"
    data = {"$schema": schema_path.as_uri(), "name": "test"}
    if case == "invalid-value":
        data["name"] = 42
    elif case == "missing-schema":
        data = {"name": "test"}
    elif case == "array":
        data = []
    elif case == "missing-reference":
        data["$schema"] = (tmp_path / "missing-schema.json").as_uri()
    if case == "invalid-json":
        path.write_text("not JSON", encoding="utf-8")
    elif case != "missing-file":
        path.write_text(json.dumps(data), encoding="utf-8")

    result = run_cli(*args, str(path))

    assert result.returncode == expected, result.stdout + result.stderr


def test_installed_cli_checks_files_after_failure(
    tmp_path: Path, schema_path: Path
) -> None:
    valid = tmp_path / "valid.json"
    valid.write_text(
        json.dumps({"$schema": schema_path.as_uri(), "name": "test"}),
        encoding="utf-8",
    )

    result = run_cli(str(tmp_path / "missing.json"), str(valid))

    assert result.returncode == 1
    assert "File not found" in result.stdout
    assert f"{valid}: Schema validation passed" in result.stdout


@pytest.mark.parametrize("expand", [False, True])
def test_installed_cli_env_expansion(
    tmp_path: Path, schema_path: Path, expand: bool
) -> None:
    directory = tmp_path / "schema `$literal'"
    directory.mkdir()
    target = directory / "schema.json"
    schema_path.rename(target)
    path = tmp_path / "input `$literal'.json"
    path.write_text(
        json.dumps({"$schema": "${SCHEMA_DIR}/schema.json", "name": "test"}),
        encoding="utf-8",
    )
    args = ["--expand-env-vars"] if expand else []

    result = run_cli(
        *args, str(path), env={**os.environ, "SCHEMA_DIR": str(directory)}
    )

    assert result.returncode == (0 if expand else 1), result.stdout + result.stderr
