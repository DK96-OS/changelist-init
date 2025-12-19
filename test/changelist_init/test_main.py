""" Testing Main Module
"""
import sys
from pathlib import Path
import subprocess

import pytest
from changelist_data.storage.storage_type import CHANGELISTS_FILE_PATH_STR

from changelist_init.__main__ import main


# The Size of the initial Changelist Data XML File, containing the empty Default Changelist.
INITIAL_EMPTY_FILE_SIZE = 172


def test_main_not_repo_raises_exit(temp_cwd):
    with pytest.raises(SystemExit, match='Git Status Runner Error:'):
        main()


def test_main_no_cl_data_file_creates_new_empty_changelists_data_file(temp_cwd):
    subprocess.run(['git', 'init'], capture_output=True)
    main()
    assert (cl_data_file := Path(CHANGELISTS_FILE_PATH_STR)).exists()
    file_contents = cl_data_file.read_text()
    assert len(file_contents) == INITIAL_EMPTY_FILE_SIZE


def test_main_single_untracked_repo_ignores_untracked_file(
    single_untracked_repo,
    git_status_line_untracked_setup
):
    main()
    assert (cl_data_file := Path(CHANGELISTS_FILE_PATH_STR)).exists()
    file_contents = cl_data_file.read_text()
    assert len(file_contents) == INITIAL_EMPTY_FILE_SIZE


def test_main_untracked_arg_single_untracked_repo_includes_untracked_file(
    single_untracked_repo,
    git_status_line_untracked_setup
):
    sys.argv.append('-u')
    main()
    assert (cl_data_file := Path(CHANGELISTS_FILE_PATH_STR)).exists()
    file_contents = cl_data_file.read_text()
    assert len(file_contents) == INITIAL_EMPTY_FILE_SIZE + 62 # The size of the additional untracked file xml.
