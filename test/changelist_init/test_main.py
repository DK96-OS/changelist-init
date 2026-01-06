""" Testing Main Module
"""
import sys
from pathlib import Path

import pytest
from changelist_data.storage.storage_type import CHANGELISTS_FILE_PATH_STR, WORKSPACE_FILE_PATH_STR

from changelist_init.__main__ import main
from test.changelist_init.conftest import write_workspace_file, MINIMUM_WORKSPACE_XML_FILE_CONTENTS, \
    DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS


# The Size of the initial Changelist Data XML File, containing the empty Default Changelist.
INITIAL_EMPTY_FILE_SIZE = 172

CHANGELIST_DATA_PATH = Path(CHANGELISTS_FILE_PATH_STR)
WORKSPACE_DATA_PATH = Path(WORKSPACE_FILE_PATH_STR)


def test_main_not_repo_raises_exit(temp_cwd):
    sys.argv = ['changelist-init']
    with pytest.raises(SystemExit, match='Git Status Runner Error:'):
        main()


def test_main_no_cl_data_file_creates_new_empty_changelists_data_file(temp_cwd_repo):
    sys.argv = ['changelist-init']
    main()
    assert CHANGELIST_DATA_PATH.exists()
    assert len(CHANGELIST_DATA_PATH.read_text()) == INITIAL_EMPTY_FILE_SIZE


def test_main_workspace_no_idea_file_creates_new_empty_changelists_data_file(temp_cwd_repo):
    sys.argv = ['changelist-init', '-w']
    main()
    # CL-Init does not create new Workspace files, even if workspace_overwrite if enabled.
    assert CHANGELIST_DATA_PATH.exists()
    assert len(CHANGELIST_DATA_PATH.read_text()) == INITIAL_EMPTY_FILE_SIZE


@pytest.mark.parametrize(
    'changelists_file_present', [
        (False,),
        (True,),
    ]
)
def test_main_workspace_file_present_is_overwrite_protected_cl_data_file_is_created_or_updated(
    temp_cwd_repo, empty_changelists_xml, default_changelists_xml, changelists_file_present,
):
    sys.argv = ['changelist-init']
    write_workspace_file(MINIMUM_WORKSPACE_XML_FILE_CONTENTS)
    # Whether the CL-Data file exists beforehand, does not change the result.
    if changelists_file_present:
        Path('.changelists').mkdir()
        CHANGELIST_DATA_PATH.touch()
        CHANGELIST_DATA_PATH.write_text(empty_changelists_xml)
    main()
    assert CHANGELIST_DATA_PATH.exists()
    assert CHANGELIST_DATA_PATH.read_text() == default_changelists_xml  # Always updated with Default Cl


@pytest.mark.parametrize(
    'changelists_file_present', [
        (False,),
        (True,),
    ]
)
def test_main_enable_workspace_overwrite_workspace_file_present_is_updated_cl_data_file_is_ignored(
    temp_cwd_repo, empty_changelists_xml, default_changelists_xml, changelists_file_present,
):
    sys.argv = ['changelist-init', '--enable_workspace_overwrite']  # or simply -w
    write_workspace_file(MINIMUM_WORKSPACE_XML_FILE_CONTENTS)
    # Whether the CL-Data file exists does not change the result.
    if changelists_file_present:
        Path('.changelists').mkdir()
        CHANGELIST_DATA_PATH.touch()
        CHANGELIST_DATA_PATH.write_text(empty_changelists_xml)
    #
    main()
    if CHANGELIST_DATA_PATH.exists():
        assert CHANGELIST_DATA_PATH.read_text() == empty_changelists_xml  # Not Modified
    # Check Workspace File
    assert WORKSPACE_DATA_PATH.exists()
    assert WORKSPACE_DATA_PATH.read_text() == DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS


def test_main_workspace_minimum_workspace_xml_empty_repo_adds_default_cl(temp_cwd_repo):
    write_workspace_file(MINIMUM_WORKSPACE_XML_FILE_CONTENTS)
    sys.argv = ['changelist-init', '-w']
    main()
    # Adds the Default Changelist
    assert WORKSPACE_DATA_PATH.read_text() == DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS


def test_main_workspace_default_cl_workspace_xml_empty_repo_has_same_contents(temp_cwd_repo):
    write_workspace_file(DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS)
    sys.argv = ['changelist-init', '-w']
    main()
    # No Changes to File Contents.
    assert WORKSPACE_DATA_PATH.read_text() == DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS
    # And the Changelist Data file was not written to.
    assert not CHANGELIST_DATA_PATH.exists()


def test_main_single_untracked_repo_ignores_untracked_file(
    single_untracked_repo,
):
    sys.argv = ['changelist-init']
    main()
    assert CHANGELIST_DATA_PATH.exists()
    assert len(CHANGELIST_DATA_PATH.read_text()) == INITIAL_EMPTY_FILE_SIZE


def test_main_untracked_arg_single_untracked_repo_includes_untracked_file(
    single_untracked_repo,
):
    sys.argv = ['changelist-init', '-u']
    main()
    assert CHANGELIST_DATA_PATH.exists()
    file_contents = CHANGELIST_DATA_PATH.read_text()
    assert '<list default="true" id="4a74640f-90b3-86a1-ab28-af29299c84fd" name="Initial Changelist" comment="">' in file_contents
    assert '<change afterPath="/setup.py" afterDir="false" />' in file_contents
    assert len(file_contents) == INITIAL_EMPTY_FILE_SIZE + 62 # The size of the additional untracked file xml.


def test_main_single_staged_modify_repo_(
    single_staged_modify_repo,
):
    sys.argv = ['changelist-init']
    main()
    assert CHANGELIST_DATA_PATH.exists()
    file_contents = CHANGELIST_DATA_PATH.read_text()
    assert '<list default="true" id="4a74640f-90b3-86a1-ab28-af29299c84fd" name="Initial Changelist" comment="">' in file_contents
    assert '<change beforePath="/setup.py" beforeDir="false" afterPath="/setup.py" afterDir="false" />' in file_contents


def test_main_single_staged_delete_repo_(
    single_staged_delete_repo,
):
    sys.argv = ['changelist-init']
    main()
    assert CHANGELIST_DATA_PATH.exists()
    file_contents = CHANGELIST_DATA_PATH.read_text()
    assert '<list default="true" id="4a74640f-90b3-86a1-ab28-af29299c84fd" name="Initial Changelist" comment="">' in file_contents
    assert '<change beforePath="/setup.py" beforeDir="false" />' in file_contents
