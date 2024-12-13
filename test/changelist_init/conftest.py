""" Test Data Provider
"""
from typing import Callable
from unittest.mock import Mock

import pytest

from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange

from changelist_init import InputData


FC_PATH_SETUP = '/setup.py'
FC_PATH_REQUIREMENTS = '/requirements.txt'

_SAMPLE_FC_0 = FC_PATH_SETUP
_SAMPLE_FC_1 = "/test/__init__.py"
_SAMPLE_FC_2 = "/test/test_method_initialize_file_changes.py"


def _sample_fc_n(n: int = 1) -> str:
    return f"/src/source_file{n}.py"


def create_fc(path: str = _SAMPLE_FC_0) -> FileChange:
    return FileChange(after_path=path, after_dir=False)


def update_fc(path: str = _SAMPLE_FC_0) -> FileChange:
    return FileChange(before_path=path, before_dir=False, after_path=path, after_dir=False)


def delete_fc(path: str = _SAMPLE_FC_0) -> FileChange:
    return FileChange(before_path=path, before_dir=False)


def get_default_cl(changes: list[FileChange] | None = None):
    return Changelist(
        id="12345678", name="Initial Changelist",
        changes=changes if changes is not None else [],
        is_default=True,
    )


def get_root_cl(changes: list[FileChange] | None = None):
    return Changelist(
        id="12", name="Project Root",
        changes=changes if changes is not None else []
    )


def get_test_cl(changes: list[FileChange] | None = None):
    return Changelist(
        id="2124", name="Test",
        changes=changes if changes is not None else []
    )


def root_cl_create_file():
    return get_root_cl([create_fc()])


def root_cl_update_file():
    return get_root_cl([update_fc()])


def root_cl_delete_file():
    return get_root_cl([delete_fc()])


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
            output.append(create_fc(get_sample_fc_path(i)))
        elif c == 'u':
            output.append(update_fc(get_sample_fc_path(i)))
        elif c == 'd':
            output.append(delete_fc(get_sample_fc_path(i)))
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
