""" Testing Git Status Reader Methods.
"""
from changelist_init.git import status_reader
from changelist_init.git.status_reader import read_git_status_line
from changelist_init.git.status_reader import read_git_status_output

from test.changelist_init.conftest import GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_line_empty_str_returns_none():
    assert read_git_status_line("") is None


def test_read_git_status_line_directory_returns_none():
    assert read_git_status_line("a_directory/") is None


def test_read_git_status_line_nested_directory_returns_none():
    assert read_git_status_line("a/directory/") is None


def test_read_git_status_line_single_untracked(
    git_status_line_untracked_setup
):
    result = read_git_status_line(git_status_line_untracked_setup)
    assert result.code == '??'
    assert result.file_path == GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_line_single_unstaged_create(
    git_status_line_unstaged_create_setup
):
    result = read_git_status_line(git_status_line_unstaged_create_setup)
    assert result.code == ' A'
    assert result.file_path == GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_line_single_unstaged_modify(
    git_status_line_unstaged_modify_setup
):
    result = status_reader.read_git_status_line(git_status_line_unstaged_modify_setup)
    assert result.code == ' M'
    assert result.file_path == GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_line_single_staged_create(
    git_status_line_staged_create_setup
):
    result = status_reader.read_git_status_line(git_status_line_staged_create_setup)
    assert result.code == 'A '
    assert result.file_path == GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_line_single_staged_modify(
    git_status_line_staged_modify_setup
):
    result = status_reader.read_git_status_line(git_status_line_staged_modify_setup)
    assert result.code == 'M '
    assert result.file_path == GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_line_single_partial_staged_create(
    git_status_line_partial_staged_create_setup
):
    result = status_reader.read_git_status_line(git_status_line_partial_staged_create_setup)
    assert result.code == 'MA'
    assert result.file_path == GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_line_single_partial_staged_modify(
    git_status_line_partial_staged_modify_setup
):
    result = status_reader.read_git_status_line(git_status_line_partial_staged_modify_setup)
    assert result.code == 'MM'
    assert result.file_path == GIT_STATUS_FILE_PATH_SETUP


def test_read_git_status_output_multi_untracked_returns_git_status_lists(
    git_status_line_multi_untracked
):
    result = read_git_status_output(git_status_line_multi_untracked)
    assert len(list(result.merge_all())) == 2


def test_read_git_status_output_multi_unstaged_create_returns_git_status_lists(
    git_status_line_multi_unstaged_create
):
    result = read_git_status_output(git_status_line_multi_unstaged_create)
    assert len(list(result.merge_all())) == 2


def test_read_git_status_output_multi_staged_create_returns_git_status_lists(
    git_status_line_multi_staged_create
):
    result = read_git_status_output(git_status_line_multi_staged_create)
    assert len(list(result.merge_all())) == 2
