""" Testing changelist_init Package-Level Method initialize_file_changes.
"""
import subprocess
from typing import Callable

import pytest

from changelist_init import initialize_file_changes

from test.changelist_init.conftest import FC_PATH_SETUP


def wrap_stdout(out: str):
    """Wrap a string in a CompletedProcess object, as if it were stdout.
    """
    return subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=out,
    )


def mock_subprocess(output: str) -> Callable:
    return lambda **kwargs: wrap_stdout(output)


def test_initialize_file_changes_tracked_only_given_single_untracked_returns_empty_list(
    input_tracked,
    git_status_line_untracked_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_untracked_setup))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 0


def test_initialize_file_changes_all_changes_given_single_untracked_returns_file_change(
    input_all,
    git_status_line_untracked_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_untracked_setup))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_tracked_only_given_single_unstaged_create_returns_file_change(
    input_tracked,
    git_status_line_unstaged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_create_setup))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_all_changes_given_single_unstaged_create_returns_file_change(
    input_all,
    git_status_line_unstaged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_create_setup))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_tracked_only_given_single_staged_create_returns_file_change(
    input_tracked,
    git_status_line_staged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_create_setup))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_all_changes_given_single_staged_create_returns_file_change(
    input_all,
    git_status_line_staged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_create_setup))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_tracked_only_given_single_unstaged_modify_returns_file_change(
    input_tracked,
    git_status_line_unstaged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_modify_setup))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_all_changes_given_single_unstaged_modify_returns_file_change(
    input_all,
    git_status_line_unstaged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_modify_setup))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_tracked_only_given_single_staged_modify_returns_file_change(
    input_tracked,
    git_status_line_staged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_modify_setup))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_all_changes_given_single_staged_modify_returns_file_change(
    input_all,
    git_status_line_staged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_modify_setup))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_initialize_file_changes_tracked_only_given_multi_init_this_returns_file_changes(
    input_tracked,
    git_status_line_multi_init_this
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_multi_init_this))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 32


def test_initialize_file_changes_all_changes_given_multi_init_this_returns_file_changes(
    input_all,
    git_status_line_multi_init_this
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_multi_init_this))
        result = initialize_file_changes(input_all)
    # Includes untracked files, but ignores Directories
    assert len(result) == 33
