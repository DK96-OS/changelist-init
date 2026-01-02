""" Testing Git Status Runner.
"""
import subprocess

import pytest

from changelist_init.git.status_runner import run_git_status


def test_run_git_status_empty_dir_raises_exit_not_a_git_repo(temp_cwd):
    with pytest.raises(SystemExit):
        run_git_status()


def test_run_git_status_empty_git_repo(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=True)
    assert len(run_git_status()) == 0


def test_run_git_status_include_untracked_empty_git_repo(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=True)
    assert len(run_git_status(include_untracked=True)) == 0


def test_run_git_status_single_untracked_returns_empty_str(
    single_untracked_repo,
    git_status_line_untracked_setup
):
    result = run_git_status()
    assert result == ""


def test_run_git_status_include_untracked_single_untracked_returns_untracked(
    single_untracked_repo,
    git_status_line_untracked_setup
):
    result = run_git_status(include_untracked=True)
    assert result == git_status_line_untracked_setup + "\n"


def test_run_git_status_single_unstaged_modify_returns_unstaged_modify(
    single_unstaged_modify_repo,
    git_status_line_unstaged_modify_setup
):
    result = run_git_status()
    assert result == git_status_line_unstaged_modify_setup + "\n"


def test_run_git_status_include_untracked_single_unstaged_modify_returns_unstaged_modify(
    single_unstaged_modify_repo,
    git_status_line_unstaged_modify_setup
):
    result = run_git_status(include_untracked=True)
    assert result == git_status_line_unstaged_modify_setup + "\n"


def test_run_git_status_single_staged_create_returns_staged_create(
    single_staged_modify_repo,
    git_status_line_staged_modify_setup
):
    result = run_git_status()
    assert result == git_status_line_staged_modify_setup + "\n"


def test_run_git_status_include_untracked_single_staged_create_returns_staged_create(
    single_staged_modify_repo,
    git_status_line_staged_modify_setup
):
    result = run_git_status(include_untracked=True)
    assert result == git_status_line_staged_modify_setup + "\n"


def test_run_git_status_single_unstaged_delete_returns_unstaged_delete(
    single_unstaged_delete_repo,
    git_status_line_unstaged_delete_setup
):
    result = run_git_status()
    assert result == git_status_line_unstaged_delete_setup + "\n"


def test_run_git_status_include_untracked_single_unstaged_delete_returns_unstaged_delete(
    single_unstaged_delete_repo,
    git_status_line_unstaged_delete_setup
):
    result = run_git_status(include_untracked=True)
    assert result == git_status_line_unstaged_delete_setup + "\n"


def test_run_git_status_single_staged_delete_returns_staged_create(
    single_staged_delete_repo,
    git_status_line_staged_delete_setup
):
    result = run_git_status()
    assert result == git_status_line_staged_delete_setup + "\n"


def test_run_git_status_include_untracked_single_staged_delete_returns_staged_create(
    single_staged_delete_repo,
    git_status_line_staged_delete_setup
):
    result = run_git_status(include_untracked=True)
    assert result == git_status_line_staged_delete_setup + "\n"


def test_run_git_status_single_unstaged_plus_multi_files_in_new_dir(
    single_unstaged_plus_multi_files_in_new_dir_repo,
    git_status_line_unstaged_modify_setup
):
    result = run_git_status()
    assert result == git_status_line_unstaged_modify_setup + '\n'


def test_run_git_status_single_unstaged_plus_multi_files_in_new_dir_include_untracked_returns_untracked_single_and_new_dir(
    single_unstaged_plus_multi_files_in_new_dir_repo,
    git_status_line_unstaged_modify_setup
):
    result = run_git_status(include_untracked=True)
    assert result == f"""{git_status_line_unstaged_modify_setup}
?? test/__init__.py
?? test/source_file.py
"""


def test_run_git_status_single_staged_plus_multi_files_in_new_dir_returns_empty_str(
    single_staged_modify_repo_plus_multi_files_in_new_dir_repo,
    git_status_line_staged_modify_setup
):
    result = run_git_status()
    assert result == f"{git_status_line_staged_modify_setup}\n"


def test_run_git_status_single_staged_plus_multi_files_in_new_dir_include_untracked_returns_untracked(
    single_staged_modify_repo_plus_multi_files_in_new_dir_repo,
    git_status_line_staged_modify_setup
):
    result = run_git_status(include_untracked=True)
    assert result == f"""{git_status_line_staged_modify_setup}
?? test/__init__.py
?? test/source_file.py
"""
