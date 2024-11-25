""" Testing Git Status Runner.
"""
import subprocess

from changelist_init.git.status_runner import run_git_status, run_untracked_status


def test_run_git_status_empty_dir_raises_exit_not_a_git_repo(
    temp_cwd
):
    try:
        run_git_status()
        raises_exit = False
    except SystemExit:
        raises_exit = True
    assert raises_exit


def test_run_git_status_empty_git_repo(
    temp_cwd
):
    subprocess.run(['git', 'init'], capture_output=True)
    assert len(run_git_status()) == 0


def test_run_git_status_single_untracked_returns_untracked(
    single_untracked_repo,
    git_status_line_untracked_setup
):
    assert run_git_status() == git_status_line_untracked_setup + "\n"


def test_run_git_status_single_unstaged_modify_returns_unstaged_modify(
    single_unstaged_modify_repo,
    git_status_line_unstaged_modify_setup
):
    assert run_git_status() == git_status_line_unstaged_modify_setup + "\n"


def test_run_git_status_single_staged_create_returns_staged_create(
    single_staged_modify_repo,
    git_status_line_staged_modify_setup
):
    assert run_git_status() == git_status_line_staged_modify_setup + "\n"


def test_run_git_status_single_unstaged_delete_returns_unstaged_delete(
    single_unstaged_delete_repo,
    git_status_line_unstaged_delete_setup
):
    assert run_git_status() == git_status_line_unstaged_delete_setup + "\n"


def test_run_git_status_single_staged_delete_returns_staged_create(
    single_staged_delete_repo,
    git_status_line_staged_delete_setup
):
    assert run_git_status() == git_status_line_staged_delete_setup + "\n"


def test_run_git_status_multi_files_in_new_dir_returns_untracked_single_and_new_dir(
    single_unstaged_plus_multi_files_in_new_dir_repo,
    git_status_line_untracked_setup
):
    assert run_git_status() == f"""{git_status_line_untracked_setup}
?? test/
"""


def test_run_untracked_status_empty_git_repo(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=True)
    result = run_untracked_status()
    assert len(result) == 0


def test_run_untracked_status_single_untracked_returns_unstaged_create(
    single_untracked_repo,
    git_status_line_unstaged_create_setup
):
    assert run_untracked_status() == git_status_line_unstaged_create_setup + "\n"


def test_run_untracked_status_single_unstaged_modify_returns_unstaged_modify(
    single_unstaged_modify_repo,
    git_status_line_unstaged_modify_setup
):
    assert run_untracked_status() == git_status_line_unstaged_modify_setup + "\n"


def test_run_untracked_status_single_staged_modify_returns_staged_modify(
    single_staged_modify_repo,
    git_status_line_staged_modify_setup
):
    assert run_untracked_status() == git_status_line_staged_modify_setup + "\n"


def test_run_untracked_status_single_unstaged_delete_returns_staged_delete(
    single_unstaged_delete_repo,
    git_status_line_staged_delete_setup
):
    # The Git Add operation seems to stage deleted files
    assert run_untracked_status() == git_status_line_staged_delete_setup + "\n"


def test_run_untracked_status_single_staged_delete_returns_staged_delete(
    single_staged_delete_repo,
    git_status_line_staged_delete_setup
):
    assert run_untracked_status() == git_status_line_staged_delete_setup + "\n"


def test_run_untracked_status_multi_files_in_new_dir_returns_staged_create(
    single_unstaged_plus_multi_files_in_new_dir_repo,
    git_status_line_unstaged_create_setup
):
    assert run_untracked_status() == f"""{git_status_line_unstaged_create_setup}
 A test/__init__.py
 A test/source_file.py
"""
