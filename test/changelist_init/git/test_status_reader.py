""" Testing Git Status Reader Methods.
"""
from changelist_init.git import status_reader
from changelist_init.git.status_reader import read_git_status_output
from test.changelist_init.git import provider


def test_read_git_status_line_empty():
    result = status_reader.read_git_status_line(provider.empty_status())
    assert result is None


def test_read_git_status_line_single_untracked():
    result = status_reader.read_git_status_line(provider.single_untracked())
    assert result.code == '??'
    assert result.file_path == provider.SINGLE_FILE_PATH


def test_read_git_status_line_single_unstaged_create():
    result = status_reader.read_git_status_line(provider.single_unstaged_create())
    assert result.code == ' A'
    assert result.file_path == provider.SINGLE_FILE_PATH


def test_read_git_status_line_single_unstaged_modify():
    result = status_reader.read_git_status_line(provider.single_unstaged_modify())
    assert result.code == ' M'
    assert result.file_path == provider.SINGLE_FILE_PATH


def test_read_git_status_line_single_staged_create():
    result = status_reader.read_git_status_line(provider.single_staged_create())
    assert result.code == 'A '
    assert result.file_path == provider.SINGLE_FILE_PATH


def test_read_git_status_line_single_staged_modify():
    result = status_reader.read_git_status_line(provider.single_staged_modify())
    assert result.code == 'M '
    assert result.file_path == provider.SINGLE_FILE_PATH


def test_read_git_status_line_single_partial_staged_create():
    result = status_reader.read_git_status_line(provider.single_partial_staged_create())
    assert result.code == 'MA'
    assert result.file_path == provider.SINGLE_FILE_PATH


def test_read_git_status_line_single_partial_staged_modify():
    result = status_reader.read_git_status_line(provider.single_partial_staged_modify())
    assert result.code == 'MM'
    assert result.file_path == provider.SINGLE_FILE_PATH


def test_read_git_status_output_multi_untracked_returns_git_status_lists():
    result = read_git_status_output(provider.multi_untracked())
    assert len(list(result.merge_all())) == 2


def test_read_git_status_output_multi_unstaged_create_returns_git_status_lists():
    result = read_git_status_output(provider.multi_unstaged_create())
    assert len(list(result.merge_all())) == 2


def test_read_git_status_output_multi_staged_create_returns_git_status_lists():
    result = read_git_status_output(provider.multi_staged_create())
    assert len(list(result.merge_all())) == 2
