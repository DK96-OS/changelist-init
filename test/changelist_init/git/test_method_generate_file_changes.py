""" Testing changelist_init Package-Level Method: generate_file_changes.
"""
import subprocess
from pathlib import Path
from typing import Callable

import pytest
from changelist_data.file_change import create_fc, update_fc

from changelist_init.git import generate_file_changes

from test.changelist_init.conftest import FC_PATH_SETUP, _SAMPLE_FC_0, _SAMPLE_FC_1, _SAMPLE_FC_2


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


def test_generate_file_changes_all_changes_given_single_untracked_returns_file_change(
    input_all,
    git_status_line_untracked_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_untracked_setup))
        result = list(generate_file_changes(input_all.include_untracked))
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_tracked_only_given_single_unstaged_create_returns_file_change(
    git_status_line_unstaged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_create_setup))
        result = list(generate_file_changes(False))
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_all_changes_given_single_unstaged_create_returns_file_change(
    git_status_line_unstaged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_create_setup))
        result = list(generate_file_changes(True))
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_tracked_only_given_single_staged_create_returns_file_change(
    git_status_line_staged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_create_setup))
        result = list(generate_file_changes(False))
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_all_changes_given_single_staged_create_returns_file_change(
    git_status_line_staged_create_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_create_setup))
        result = list(generate_file_changes(True))
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_tracked_only_given_single_unstaged_modify_returns_file_change(
    git_status_line_unstaged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_modify_setup))
        result = list(generate_file_changes(False))
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_all_changes_given_single_unstaged_modify_returns_file_change(
    git_status_line_unstaged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_unstaged_modify_setup))
        result = list(generate_file_changes(True))
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_tracked_only_given_single_staged_modify_returns_file_change(
    git_status_line_staged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_modify_setup))
        result = list(generate_file_changes(False))
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_all_changes_given_single_staged_modify_returns_file_change(
    git_status_line_staged_modify_setup
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_staged_modify_setup))
        result = list(generate_file_changes(True))
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path
    assert result[0].after_path == FC_PATH_SETUP


def test_generate_file_changes_all_changes_given_multi_init_this_returns_file_changes(
    git_status_line_multi_init_this
):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', mock_subprocess(git_status_line_multi_init_this))
        result = list(generate_file_changes(True))
    # Includes untracked files, but ignores Directories
    assert len(result) == 33


def test_generate_file_changes_not_a_repo_raises_exit(temp_cwd):
    with pytest.raises(SystemExit):
        list(generate_file_changes(False))


def test_generate_file_changes_init_repo_returns_empty_list(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    result = list(generate_file_changes(False))
    assert result == []


def test_generate_file_changes_single_untracked_repo_ignore_untracked_returns_empty_list(
    single_untracked_repo
):
    result = list(generate_file_changes(False))
    assert result == []


def test_generate_file_changes_single_untracked_repo_include_untracked_returns_empty_list(
    single_untracked_repo
):
    result = list(generate_file_changes(True))
    assert result == [create_fc(_SAMPLE_FC_0)]


def test_generate_file_changes_single_unstaged_plus_multi_files_in_new_dir_ignore_untracked_returns_empty_list(
    single_unstaged_plus_multi_files_in_new_dir_repo
):
    result = list(generate_file_changes(False))
    assert result == [update_fc(_SAMPLE_FC_0)]


def test_generate_file_changes_single_untracked_plus_multi_files_in_new_dir_include_untracked_returns_empty_list(
    single_unstaged_plus_multi_files_in_new_dir_repo
):
    result = list(generate_file_changes(True))
    assert result == [update_fc(_SAMPLE_FC_0), create_fc(_SAMPLE_FC_1), create_fc(_SAMPLE_FC_2)]


@pytest.mark.parametrize(
    'file_count', [1, 10]
)
def test_generate_file_changes_init_repo_touch_files_returns_status_lists(file_count, temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count):
        (root_dir / f'new_python_file{i}.py').touch()
    #
    result = list(generate_file_changes(include_untracked=False))
    assert len(result) == 0


@pytest.mark.parametrize(
    'file_count', [1, 10]
)
def test_generate_file_changes_include_untracked_init_repo_touch_files_returns_status_lists(file_count, temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count):
        (root_dir / f'new_python_file{i}.py').touch()
    #
    result = list(generate_file_changes(include_untracked=True))
    assert len(result) == file_count


def test_generate_file_changes_init_repo_touch_files_add_half_ignore_untracked_returns_half(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count := 10):
        (root_dir / f'new_python_file{i}.py').touch()
        (root_dir / f'new_java_file{i}.java').touch()
    subprocess.run(['git', 'add', 'new_python*'], capture_output=True)
    #
    result = list(generate_file_changes(include_untracked=False))
    assert len(result) == file_count


def test_generate_file_changes_init_repo_touch_files_add_half_include_untracked_returns_all(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=False)
    root_dir = Path(temp_cwd.name)
    for i in range(file_count := 10):
        (root_dir / f'new_python_file{i}.py').touch()
        (root_dir / f'new_java_file{i}.java').touch()
    subprocess.run(['git', 'add', 'new_python*'], capture_output=True)
    #
    result = list(generate_file_changes(include_untracked=True))
    assert len(result) == 2 * file_count
