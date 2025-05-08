import subprocess
from unittest.mock import patch, MagicMock
from typing import Any, Set

import pytest  # type: ignore

from pre_commit_hook_mypy.mypy_committed import (  # type: ignore
    get_modified_files,
    run_mypy,
    filter_output_for_committed_files,
    main,
)


def test_given_git_diff_when_get_modified_files_then_returns_py_files() -> None:
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "file1.py\nfile2.txt\nfile3.py\n"
        mock_run.return_value = mock_result

        result = get_modified_files()

        assert result == {"file1.py", "file3.py"}
        mock_run.assert_called_once()


def test_given_subprocess_error_when_get_modified_files_then_returns_empty_set() -> (
    None
):
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "git")

        result = get_modified_files()

        assert result == set()


def test_given_valid_args_when_run_mypy_then_returns_exit_code_and_output() -> None:
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = (
            "file1.py:10: error: Type error\nfile2.py:20: error: Another error"
        )
        mock_run.return_value = mock_result

        exit_code, output = run_mypy(["file1.py", "file2.py"])

        assert exit_code == 1
        assert len(output) == 2
        assert "file1.py:10: error: Type error" in output
        mock_run.assert_called_once()


def test_given_mypy_not_found_when_run_mypy_then_returns_error() -> None:
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError

        exit_code, output = run_mypy(["file.py"])

        assert exit_code == 1
        assert output == []


def test_given_output_lines_when_filter_output_for_committed_files_then_returns_filtered_lines() -> (
    None
):
    output_lines = [
        "file1.py:10: error: Type error",
        "file2.py:20: error: Another error",
        "Something else",
    ]
    committed_files = {"file1.py"}

    result = filter_output_for_committed_files(output_lines, committed_files)

    assert len(result) == 1
    assert "file1.py:10: error: Type error" in result


def test_given_windows_paths_when_filter_output_for_committed_files_then_normalizes_paths() -> (
    None
):
    output_lines = [
        "dir\\file1.py:10: error: Type error",
        "dir/file2.py:20: error: Another error",
    ]
    committed_files = {"dir/file1.py"}

    result = filter_output_for_committed_files(output_lines, committed_files)

    assert len(result) == 1
    assert "dir\\file1.py:10: error: Type error" in result


def test_given_no_committed_files_when_main_then_returns_zero() -> None:
    with patch(
        "pre_commit_hook_mypy.mypy_committed.get_modified_files"
    ) as mock_get_files:
        mock_get_files.return_value = set()

        with patch("sys.argv", ["mypy-committed"]):
            result = main()

        assert result == 0


def test_given_no_mypy_errors_when_main_then_returns_zero() -> None:
    with patch(
        "pre_commit_hook_mypy.mypy_committed.get_modified_files"
    ) as mock_get_files:
        mock_get_files.return_value = {"file1.py"}

        with patch("pre_commit_hook_mypy.mypy_committed.run_mypy") as mock_run_mypy:
            mock_run_mypy.return_value = (0, [])

            with patch("sys.argv", ["mypy-committed"]):
                result = main()

            assert result == 0
