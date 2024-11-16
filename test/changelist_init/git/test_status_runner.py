"""
"""
import os
import subprocess
import tempfile
from pathlib import Path
import pytest

from changelist_init.git.status_runner import run_git_status, run_untracked_status
from test.changelist_init.git import provider


@pytest.fixture
def temp_cwd():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    yield dir
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_untracked_repo():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    subprocess.run(['git', 'init'], capture_output=True,)
    # Setup Files
    setup_file = Path(tdir.name + "/setup.py")
    setup_file.touch()
    setup_file.write_text("Hellow")
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_unstaged_modify_repo():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    subprocess.run(['git', 'init'], capture_output=True,)
    # Setup Files
    setup_file = Path(tdir.name + "/setup.py")
    setup_file.touch()
    setup_file.write_text("Hellow")
    # Setup Git Config
    subprocess.run(['git', 'config', '--add', 'user.name', 'username101'])
    subprocess.run(['git', 'config', '--add', 'user.email', 'email@provider.com'])
    # Commit
    subprocess.run(['git', 'add', 'setup.py'],
        capture_output=True,)
    subprocess.run(['git', 'commit', '-m', '"Init!"'],
        capture_output=True,)
    # Modify
    setup_file.write_text("Hello World!")
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_staged_modify_repo():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    subprocess.run(['git', 'init'], capture_output=True,)
    # Setup Files
    setup_file = Path(tdir.name + "/setup.py")
    setup_file.touch()
    setup_file.write_text("Hellow")
    # Setup Git Config
    subprocess.run(['git', 'config', '--add', 'user.name', 'username101'])
    subprocess.run(['git', 'config', '--add', 'user.email', 'email@provider.com'])
    # Commit
    subprocess.run(['git', 'add', 'setup.py'])
    subprocess.run(['git', 'commit', '-m', '"Init!"'], capture_output=True)
    # Modify
    setup_file.write_text("Hello World!")
    # Stage
    subprocess.run(['git', 'add', 'setup.py'])
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_unstaged_delete_repo():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    subprocess.run(['git', 'init'], capture_output=True,)
    # Setup Files
    setup_file = Path(tdir.name + "/setup.py")
    setup_file.touch()
    setup_file.write_text("Hellow")
    # Setup Git Config
    subprocess.run(['git', 'config', '--add', 'user.name', 'username101'])
    subprocess.run(['git', 'config', '--add', 'user.email', 'email@provider.com'])
    # Commit
    subprocess.run(['git', 'add', 'setup.py'])
    subprocess.run(['git', 'commit', '-m', '"Init!"'], capture_output=True)
    # Delete
    setup_file.unlink()
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_staged_delete_repo():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    subprocess.run(['git', 'init'],
        capture_output=True,)
    # Setup Files
    setup_file = Path(tdir.name + "/setup.py")
    setup_file.touch()
    setup_file.write_text("Hellow")
    # Setup Git Config
    subprocess.run(['git', 'config', '--add', 'user.name', 'username101'])
    subprocess.run(['git', 'config', '--add', 'user.email', 'email@provider.com'])
    # Commit
    subprocess.run(['git', 'add', 'setup.py'])
    subprocess.run(['git', 'commit', '-m', '"Init!"'], capture_output=True)
    # Modify
    setup_file.unlink()
    # Stage
    subprocess.run(['git', 'add', 'setup.py'])
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_unstaged_plus_multi_files_in_new_dir_repo():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    subprocess.run(['git', 'init'], capture_output=True,)
    # Setup Files
    setup_file = Path(tdir.name + "/setup.py")
    setup_file.touch()
    setup_file.write_text("Hellow")
    # Create new Dir
    new_dir = (setup_file.parent / "test")
    new_dir.mkdir()
    # Create Files
    new_init_file = new_dir / "__init__.py"
    new_init_file.touch()
    new_init_file.write_text('"""  """')
    new_src_file = new_dir / "source_file.py"
    new_src_file.touch()
    new_src_file.write_text("src")
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


def test_run_git_status_empty_dir_raises_exit_not_a_git_repo(temp_cwd):
    try:
        run_git_status()
        raises_exit = False
    except SystemExit:
        raises_exit = True
    assert raises_exit


def test_run_git_status_empty_git_repo(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=True)
    result = run_git_status()
    assert len(result) == 0


def test_run_git_status_single_untracked_returns_untracked(single_untracked_repo):
    result = run_git_status()
    assert result == provider.single_untracked() + "\n"


def test_run_git_status_single_unstaged_modify_returns_unstaged_modify(single_unstaged_modify_repo):
    result = run_git_status()
    assert result == provider.single_unstaged_modify() + "\n"


def test_run_git_status_single_staged_create_returns_staged_create(single_staged_modify_repo):
    result = run_git_status()
    assert result == provider.single_staged_modify() + "\n"


def test_run_git_status_single_unstaged_delete_returns_unstaged_delete(single_unstaged_delete_repo):
    result = run_git_status()
    assert result == provider.single_unstaged_delete() + "\n"


def test_run_git_status_single_staged_delete_returns_staged_create(single_staged_delete_repo):
    result = run_git_status()
    assert result == provider.single_staged_delete() + "\n"


def test_run_git_status_multi_files_in_new_dir_returns_untracked_single_and_new_dir(
        single_unstaged_plus_multi_files_in_new_dir_repo):
    result = run_git_status()
    assert result == f"""{provider.single_untracked()}
?? test/
"""


def test_run_untracked_status_empty_git_repo(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=True)
    result = run_untracked_status()
    assert len(result) == 0


def test_run_untracked_status_single_untracked_returns_unstaged_create(single_untracked_repo):
    result = run_untracked_status()
    assert result == provider.single_unstaged_create() + "\n"


def test_run_untracked_status_single_unstaged_modify_returns_unstaged_modify(single_unstaged_modify_repo):
    result = run_untracked_status()
    assert result == provider.single_unstaged_modify() + "\n"


def test_run_untracked_status_single_staged_modify_returns_staged_modify(single_staged_modify_repo):
    result = run_untracked_status()
    assert result == provider.single_staged_modify() + "\n"


def test_run_untracked_status_single_unstaged_delete_returns_staged_delete(single_unstaged_delete_repo):
    # The Git Add operation seems to stage deleted files
    result = run_untracked_status()
    assert result == provider.single_staged_delete() + "\n"


def test_run_untracked_status_single_staged_delete_returns_staged_delete(single_staged_delete_repo):
    result = run_untracked_status()
    assert result == provider.single_staged_delete() + "\n"


def test_run_untracked_status_multi_files_in_new_dir_returns_staged_create(
        single_unstaged_plus_multi_files_in_new_dir_repo):
    result = run_untracked_status()
    assert result == f"""{provider.single_unstaged_create()}
 A test/__init__.py
 A test/source_file.py
"""
