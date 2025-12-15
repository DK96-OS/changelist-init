""" Testing CL-Init Git Package Method: get_status_lists.
"""
import subprocess
from pathlib import Path

import pytest

from changelist_init.git import get_status_lists


def test_get_status_lists_not_a_repo_raises_exit(temp_cwd):
    with pytest.raises(SystemExit):
        get_status_lists()


def test_get_status_lists_init_repo_returns_status_lists(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    result = get_status_lists()
    assert result.staged == []
    assert result.unstaged == []
    assert result.untracked == []
    assert result.partial_stage == []


@pytest.mark.parametrize(
    'file_count', [
        1, 10, 100,
    ]
)
def test_get_status_lists_init_repo_touch_files_returns_status_lists(file_count, temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count):
        (root_dir / f'new_python_file{i}.py').touch()
    #
    result = get_status_lists(include_untracked=False)
    assert len(result.staged) == 0
    assert len(result.unstaged) == 0
    assert len(result.untracked) == 0
    assert len(result.partial_stage) == 0


@pytest.mark.parametrize(
    'file_count', [
        1, 10, 100,
    ]
)
def test_get_status_lists_include_untracked_init_repo_touch_files_returns_status_lists(file_count, temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count):
        (root_dir / f'new_python_file{i}.py').touch()
    #
    result = get_status_lists(include_untracked=True)
    assert len(result.staged) == 0
    assert len(result.unstaged) == 0
    assert len(result.untracked) == file_count
    assert len(result.partial_stage) == 0


@pytest.mark.parametrize(
    'file_count', [
        1, 10, 100,
    ]
)
def test_get_status_lists_init_repo_touch_files_add_all_py_returns_status_lists(file_count, temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count):
        (root_dir / f'new_python_file{i}.py').touch()
    subprocess.run(['git', 'add', 'new*'], capture_output=True)
    #
    result = get_status_lists(include_untracked=False)
    assert len(result.staged) == file_count
    assert len(result.unstaged) == 0
    assert len(result.untracked) == 0
    assert len(result.partial_stage) == 0


def test_get_status_lists_init_repo_touch_files_add_half_returns_status_lists(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count := 10):
        (root_dir / f'new_python_file{i}.py').touch()
        (root_dir / f'new_java_file{i}.java').touch()
    subprocess.run(['git', 'add', 'new_python*'], capture_output=True)
    #
    result = get_status_lists(include_untracked=True)
    assert len(result.staged) == file_count
    assert len(result.unstaged) == 0
    assert len(result.untracked) == file_count
    assert len(result.partial_stage) == 0
