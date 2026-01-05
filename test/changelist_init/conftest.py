""" Test Data Provider
"""
import os
import subprocess
import tempfile
from os import getcwd, chdir
from pathlib import Path
from typing import Callable
from unittest.mock import Mock

import pytest
from changelist_data import file_change, ChangelistDataStorage, new_tree, StorageType

from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange
from changelist_data.storage import storage_type
from changelist_data.storage.storage_type import WORKSPACE_FILE_PATH_STR

from changelist_init import InputData, data


FC_PATH_SETUP = '/setup.py'
FC_PATH_REQUIREMENTS = '/requirements.txt'

_SAMPLE_FC_0 = FC_PATH_SETUP
_SAMPLE_FC_1 = "/test/__init__.py"
_SAMPLE_FC_2 = "/test/source_file.py"


def _sample_fc_n(n: int = 1) -> str:
    return f"/src/source_file{n}.py"


def get_default_cl(changes: list[FileChange] | None = None):
    return Changelist(
        id="12345678",
        name="Initial Changelist",
        changes=changes if changes is not None else [],
        is_default=True,
    )


def get_root_cl(changes: list[FileChange] | None = None):
    return Changelist(
        id="12",
        name="Project Root",
        changes=changes if changes is not None else [],
    )


def get_test_cl(changes: list[FileChange] | None = None):
    return Changelist(
        id="2124",
        name="Test",
        changes=changes if changes is not None else [],
    )


def root_cl_create_file():
    return get_root_cl([file_change.create_fc(_SAMPLE_FC_0)])


def root_cl_update_file():
    return get_root_cl([file_change.update_fc(_SAMPLE_FC_0)])


def root_cl_delete_file():
    return get_root_cl([file_change.delete_fc(_SAMPLE_FC_0)])


def get_sample_fc_path(number: int) -> str:
    """ Obtain the string path for a sample file.
    """
    if number == 0:
        return _SAMPLE_FC_0
    elif number == 1:
        return _SAMPLE_FC_1
    elif number == 2:
        return _SAMPLE_FC_2
    else:
        return _sample_fc_n(number - 2)


def get_fc_status(number: int) -> str:
    if number == 0:
        return 'c'
    elif number == 1:
        return 'u'
    else:
        return 'd'


def get_cl(number: int, changes: list[FileChange]):
    if number == 0:
        return get_default_cl(changes)
    elif number == 1:
        return get_root_cl(changes)
    else:
        return get_test_cl(changes)


def fc_sample_list(
    fc_input: str,
) -> list[FileChange]:
    """ Create a list of FileChange sample data.
    """
    output = []
    for i, c in enumerate(fc_input):
        if c == 'c':
            output.append(file_change.create_fc(get_sample_fc_path(i)))
        elif c == 'u':
            output.append(file_change.update_fc(get_sample_fc_path(i)))
        elif c == 'd':
            output.append(file_change.delete_fc(get_sample_fc_path(i)))
        elif c == ' ':
            pass    # Skip this file path
        else:
            raise ValueError(f"Unknown FC Sample character ({c}) at index {i}.")
    return output


def cl_sample_list(
    cl_input: list[str],
) -> list[Changelist]:
    """ Create a list of Changelists containing FileChange data.
    """
    if len(cl_input) != 3:
        raise ValueError("Provide 3 strings to match 3 Changelists.")
    lists = []
    if len(default := cl_input[0]) > 0:
        lists.append(get_default_cl(fc_sample_list(default)))
    if len(root := cl_input[1]) > 0:
        lists.append(get_root_cl(fc_sample_list(root)))
    if len(test := cl_input[2]) > 0:
        lists.append(get_test_cl(fc_sample_list(test)))
    return lists


def create_sample_list_input(
    n: int,
    data: str | Callable[[int], str],
) -> list[str]:
    """
    -1 - All are empty.
    0 - The first is data.
    1 - The second is data.
    2 - The third is data.
    3+ - All are data.
    """
    return [
        '' if n != 0 and n < 3 else (data if isinstance(data, str) else data(0)),
        '' if n != 1 and n < 3 else (data if isinstance(data, str) else data(1)),
        '' if n != 2 and n < 3 else (data if isinstance(data, str) else data(2)),
    ]


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


GIT_STATUS_FILE_PATH_SETUP = 'setup.py'
GIT_STATUS_FILE_PATH_REQUIREMENTS = 'requirements.txt'


def git_status_line(code: str, file_path: str) -> str:
    return f"{code} {file_path}"


@pytest.fixture()
def git_status_line_untracked_setup():
    return git_status_line("??", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_untracked_requirements():
    return git_status_line("??", GIT_STATUS_FILE_PATH_REQUIREMENTS)


@pytest.fixture()
def git_status_line_unstaged_create_setup():
    return git_status_line(" A", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_unstaged_modify_setup():
    return git_status_line(" M", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_unstaged_delete_setup():
    return git_status_line(" D", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_staged_create_setup():
    return git_status_line("A ", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_staged_modify_setup():
    return git_status_line("M ", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_staged_delete_setup():
    return git_status_line("D ", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_partial_staged_create_setup():
    return git_status_line("MA", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_partial_staged_modify_setup():
    return git_status_line("MM", GIT_STATUS_FILE_PATH_SETUP)


@pytest.fixture()
def git_status_line_multi_untracked():
    return f"""?? {GIT_STATUS_FILE_PATH_SETUP}
?? {GIT_STATUS_FILE_PATH_REQUIREMENTS}
"""


@pytest.fixture()
def git_status_line_multi_unstaged_create():
    return f""" A {GIT_STATUS_FILE_PATH_SETUP}
 A {GIT_STATUS_FILE_PATH_REQUIREMENTS}
"""


@pytest.fixture()
def git_status_line_multi_staged_create():
    return f"""A  {GIT_STATUS_FILE_PATH_SETUP}
A  {GIT_STATUS_FILE_PATH_REQUIREMENTS}
"""


@pytest.fixture()
def git_status_line_multi_init_this():
    """ The Git Status Output from this project during the peak of init-development.
    """
    return """ M .ftb/initialize.treescript
A  .github/dependabot.yml
AM .github/workflows/ci_run.yml
A  .github/workflows/linting.yml
A  .github/workflows/publish.yml
 M .gitignore
 M README.md
AM changelist_init/__init__.py
AM changelist_init/__main__.py
AM changelist_init/git/__init__.py
AM changelist_init/git/git_file_status.py
AM changelist_init/git/git_status_lists.py
AM changelist_init/git/git_tracking_status.py
AM changelist_init/git/status_codes.py
AM changelist_init/git/status_reader.py
AM changelist_init/git/status_runner.py
AM changelist_init/input/__init__.py
AM changelist_init/input/argument_data.py
AM changelist_init/input/argument_parser.py
AM changelist_init/input/input_data.py
AM changelist_init/input/string_validation.py
A  pyproject.toml
AM requirements.txt
AM setup.py
A  test/__init__.py
A  test/changelist_init/__init__.py
A  test/changelist_init/git/__init__.py
AM test/changelist_init/git/provider.py
AM test/changelist_init/git/test_status_reader.py
A  test/changelist_init/input/__init__.py
AM test/changelist_init/input/test_string_validation.py
AM test/changelist_init/test_init.py
?? .ftb/burn.treescript
?? .idea/
?? external/
"""


@pytest.fixture
def temp_cwd():
    """ Creates a Temporary Working Directory for subprocesses.
    """
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = getcwd()
    chdir(tdir.name)
    yield tdir
    chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_untracked_repo():
    """ A Git Repo, based on temp_cwd fixture, containing a single untracked file.
    """
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    _init_and_config_git_repo()
    # Setup Files
    (setup_file := Path(tdir.name + "/setup.py")).touch()
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
    _init_and_config_git_repo()
    # Setup Files
    (setup_file := Path(tdir.name + "/setup.py")).touch()
    setup_file.write_text("Hellow")
    # Commit
    subprocess.run(['git', 'add', 'setup.py'], capture_output=True)
    subprocess.run(['git', 'commit', '-m', '"Init!"'], capture_output=True)
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
    _init_and_config_git_repo()
    # Setup Files
    (setup_file := Path(tdir.name + "/setup.py")).touch()
    setup_file.write_text("Hellow")
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
    _init_and_config_git_repo()
    # Setup Files
    (setup_file := Path(tdir.name + "/setup.py")).touch()
    setup_file.write_text("Hellow")
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
    _init_and_config_git_repo()
    # Setup Files
    (setup_file := Path(tdir.name + "/setup.py")).touch()
    setup_file.write_text("Hellow")
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
    """ Files are created with short string contents. No git add or commits.
    """
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    _init_and_config_git_repo()
    # Setup Files
    (setup_file := Path(tdir.name + "/setup.py")).touch()
    setup_file.write_text("Hellow")
    # Commit
    subprocess.run(['git', 'add', 'setup.py'])
    subprocess.run(['git', 'commit', '-m', '"Init!"'], capture_output=True)
    # Modify Setup
    setup_file.write_text('"""  """')
    # Create new Dir
    (new_dir := (setup_file.parent / "test")).mkdir()
    # Create Files
    (new_init_file := new_dir / "__init__.py").touch()
    new_init_file.write_text('"""  """')
    (new_src_file := new_dir / "source_file.py").touch()
    new_src_file.write_text("src")
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


@pytest.fixture
def single_staged_modify_repo_plus_multi_files_in_new_dir_repo():
    tdir = tempfile.TemporaryDirectory()
    initial_cwd = os.getcwd()
    os.chdir(tdir.name)
    _init_and_config_git_repo()
    # Setup Files
    (setup_file := Path(tdir.name + "/setup.py")).touch()
    setup_file.write_text("Hellow")
    # Commit
    subprocess.run(['git', 'add', 'setup.py'])
    subprocess.run(['git', 'commit', '-m', '"Init!"'], capture_output=True)
    # Modify
    setup_file.write_text("Hello World!")
    # Stage
    subprocess.run(['git', 'add', 'setup.py'])
    # Create new Dir
    (new_dir := setup_file.parent / "test").mkdir()
    # Create Files
    (new_init_file := new_dir / "__init__.py").touch()
    new_init_file.write_text('"""  """')
    (new_src_file := new_dir / "source_file.py").touch()
    new_src_file.write_text("src")
    # Ready For Test Case
    yield tdir
    # After
    os.chdir(initial_cwd)
    tdir.cleanup()


def _init_and_config_git_repo():
    subprocess.run(['git', 'init'], capture_output=True)
    subprocess.run(['git', 'config', '--add', 'user.name', 'username101'])
    subprocess.run(['git', 'config', '--add', 'user.email', 'email@provider.com'])


def construct_new_cl_data_storage() -> ChangelistDataStorage:
    """ A new empty in-memory storage object.
    """
    return ChangelistDataStorage(
        new_tree(), StorageType.CHANGELISTS, storage_type.CHANGELISTS_FILE_PATH_STR
    )


def write_workspace_file(contents: str):
    """ Write string to the default workspace file location.
 - Ensure that you use a temp_cwd with this method.
    """
    Path('.idea').mkdir()
    (workspace_path := Path(WORKSPACE_FILE_PATH_STR)).touch()
    workspace_path.write_text(contents)


MINIMUM_WORKSPACE_XML_FILE_CONTENTS = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ChangeListManager" /></project>"""


DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS = f"""<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ChangeListManager">
    <list default="true" id="{data._DEFAULT_CHANGELIST_ID}" name="{data._DEFAULT_CHANGELIST_NAME}" comment="" />
  </component></project>"""
