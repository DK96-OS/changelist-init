"""
"""
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_cwd():
    """ Creates a Temporary Working Directory for Git subprocesses.
    """
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    yield tdir
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_untracked_repo():
    """ A Git Repo, based on temp_cwd fixture, containing a single untracked file.
    """
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
