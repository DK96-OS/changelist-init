"""
"""
import subprocess
from unittest.mock import Mock

import pytest
from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange

from changelist_init import initialize_file_changes, InputData, merge_file_changes
from test.changelist_init.git import provider


@pytest.fixture()
def input_tracked():
    return InputData(
        storage=Mock(),
    )


@pytest.fixture()
def input_all():
    return InputData(
        storage=Mock(),
        include_untracked=True,
    )


def wrap_stdout(out):
    return subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=out,
    )


def test_initialize_file_changes_tracked_only_given_single_untracked_returns_empty_list(input_tracked):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_untracked()))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 0


def test_initialize_file_changes_all_changes_given_single_untracked_returns_file_change(input_all):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_untracked()))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == provider.SINGLE_FILE_PATH


def test_initialize_file_changes_tracked_only_given_single_unstaged_create_returns_file_change(input_tracked):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_unstaged_create()))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == provider.SINGLE_FILE_PATH


def test_initialize_file_changes_all_changes_given_single_unstaged_create_returns_file_change(input_all):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_unstaged_create()))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == provider.SINGLE_FILE_PATH


def test_initialize_file_changes_tracked_only_given_single_staged_create_returns_file_change(input_tracked):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_staged_create()))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == provider.SINGLE_FILE_PATH


def test_initialize_file_changes_all_changes_given_single_staged_create_returns_file_change(input_all):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_staged_create()))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].before_path is None
    assert result[0].after_path == provider.SINGLE_FILE_PATH


def test_initialize_file_changes_tracked_only_given_single_unstaged_modify_returns_file_change(input_tracked):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_unstaged_modify()))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path


def test_initialize_file_changes_all_changes_given_single_unstaged_modify_returns_file_change(input_all):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_unstaged_modify()))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path


def test_initialize_file_changes_tracked_only_given_single_staged_modify_returns_file_change(input_tracked):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_staged_modify()))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path


def test_initialize_file_changes_all_changes_given_single_staged_modify_returns_file_change(input_all):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.single_staged_modify()))
        result = initialize_file_changes(input_all)
    assert len(result) == 1
    assert result[0].after_path == result[0].before_path


def test_initialize_file_changes_tracked_only_given_multi_init_this_returns_file_changes(input_tracked):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.multi_init_this()))
        result = initialize_file_changes(input_tracked)
    assert len(result) == 32


def test_initialize_file_changes_all_changes_given_multi_init_this_returns_file_changes(input_all):
    with pytest.MonkeyPatch.context() as c:
        c.setattr(subprocess, 'run', lambda **kwargs: wrap_stdout(provider.multi_init_this()))
        result = initialize_file_changes(input_all)
    assert len(result) == 35


def test_merge_file_changes_empty_lists_returns_true():
    assert merge_file_changes([], [])


def test_merge_file_changes_empty_existing_list_returns_true():
    existing_list = []
    assert merge_file_changes(
        existing_list,
        [FileChange(after_path='hello.py', after_dir=False)]
    )
    assert len(existing_list) == 1


def test_merge_file_changes_empty_files_returns_true():
    existing_list = [Changelist('id', 'name', [])]
    assert merge_file_changes(
        existing_list,
        []
    )
    assert len(existing_list) == 1


def test_merge_file_changes_single_files_returns_true():
    existing_list = [Changelist('id', 'name', [])]
    assert merge_file_changes(
        existing_list,
        [FileChange(after_path='hello.py', after_dir=False)]
    )
    assert len(existing_list) == 1


def test_merge_file_changes_single_file_already_exists_returns_true():
    existing_list = [Changelist('id', 'name', [FileChange(after_path='hello.py', after_dir=False)])]
    assert merge_file_changes(
        existing_list,
        [FileChange(after_path='hello.py', after_dir=False)]
    )
    assert len(existing_list) == 1
