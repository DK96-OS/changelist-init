""" Test Data Provider for Git Tests.
"""


SINGLE_FILE_PATH = 'setup.py'
SECOND_FILE_PATH = 'requirements.txt'


def empty_status():
    return ""


def single_untracked():
    return "?? " + SINGLE_FILE_PATH


def single_unstaged_create():
    return " A " + SINGLE_FILE_PATH


def single_unstaged_modify():
    return " M " + SINGLE_FILE_PATH


def single_unstaged_delete():
    return " D " + SINGLE_FILE_PATH


def single_staged_create():
    return "A  " + SINGLE_FILE_PATH


def single_staged_modify():
    return "M  " + SINGLE_FILE_PATH


def single_staged_delete():
    return "D  " + SINGLE_FILE_PATH


def single_partial_staged_create():
    return "MA " + SINGLE_FILE_PATH


def single_partial_staged_modify():
    return "MM " + SINGLE_FILE_PATH


def multi_untracked():
    return f"""?? {SINGLE_FILE_PATH}
?? {SECOND_FILE_PATH}
"""

def multi_staged_create():
    return f"""A  {SINGLE_FILE_PATH}
A  {SECOND_FILE_PATH}
"""


def multi_staged_modify():
    return f"""M  {SINGLE_FILE_PATH}
M  {SECOND_FILE_PATH}
"""


def multi_unstaged_create():
    return f""" A {SINGLE_FILE_PATH}
A  {SECOND_FILE_PATH}
"""


def multi_unstaged_modify():
    return f""" M {SINGLE_FILE_PATH}
M  {SECOND_FILE_PATH}
"""

def multi_init_this():
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
