""" Testing Input Init Package Method.
"""
from pathlib import Path

import pytest
from changelist_data.storage.storage_type import CHANGELISTS_FILE_PATH_STR, WORKSPACE_FILE_PATH_STR

from changelist_init import data
from changelist_init.input import validate_input
from test.changelist_init.conftest import write_workspace_file, MINIMUM_WORKSPACE_XML_FILE_CONTENTS, \
    DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS


def test_validate_input_(temp_cwd):
    args = []
    result = validate_input(args)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_include_untracked_(temp_cwd):
    args = ['--include_untracked']
    result = validate_input(args)
    assert result.include_untracked


def test_validate_input_invalid_changelists_raises_exit(temp_cwd):
    args = ['--changelists_file', '  ']
    with pytest.raises(SystemExit):
        validate_input(args)


def test_validate_input_default_changelists_file_returns_valid_input_data(temp_cwd):
    args = ['--changelists_file', CHANGELISTS_FILE_PATH_STR]
    result = validate_input(args)
    assert result.storage.update_path == Path(CHANGELISTS_FILE_PATH_STR)
    assert not result.include_untracked


def test_validate_input_invalid_workspace_raises_exit(temp_cwd):
    args = ['--workspace_file', '  ']
    with pytest.raises(SystemExit):
        validate_input(args)


def test_validate_input_default_workspace_file_does_not_exit_raises_exit(temp_cwd):
    args = ['--workspace_file', WORKSPACE_FILE_PATH_STR]
    with pytest.raises(SystemExit, match='File did not exist.'):
        validate_input(args)


def test_validate_input_default_workspace_file_contains_incomplete_xml(temp_cwd):
    write_workspace_file('<?xml version="1.0" encoding="UTF-8"?>')
    args = ['--workspace_file', WORKSPACE_FILE_PATH_STR]
    with pytest.raises(SystemExit, match='Unable to Parse Workspace XML File.'):
        validate_input(args)


def test_validate_input_default_workspace_file_contains_minimum_xml(temp_cwd):
    # At least the ChangeListManager Component must exist
    write_workspace_file(MINIMUM_WORKSPACE_XML_FILE_CONTENTS)
    args = ['--workspace_file', WORKSPACE_FILE_PATH_STR]
    result = validate_input(args)
    assert result.storage.update_path == Path(WORKSPACE_FILE_PATH_STR)


def test_validate_input_default_workspace_file_contains_xml_cl_manager(temp_cwd):
    # At least the ChangeListManager Component must exist
    write_workspace_file(DEFAULT_CL_WORKSPACE_XML_FILE_CONTENTS)
    args = ['--workspace_file', WORKSPACE_FILE_PATH_STR]
    result = validate_input(args)
    assert result.storage.update_path == Path(WORKSPACE_FILE_PATH_STR)
    default_cl = result.storage.get_changelists()[0]
    assert default_cl.id == data._DEFAULT_CHANGELIST_ID
    assert default_cl.name == data._DEFAULT_CHANGELIST_NAME
    assert default_cl.comment == ''
    assert default_cl.is_default


def test_validate_input_invalid_arg_raises_exit(temp_cwd):
    args = ['--unknown_arg']
    with pytest.raises(SystemExit):
        validate_input(args)
