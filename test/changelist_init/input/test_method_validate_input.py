""" Testing Input Init Package Method.
"""
import pytest

from changelist_init.input import validate_input


def test_validate_input_(temp_cwd):
    args = []
    result = validate_input(args)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_include_untracked_(temp_cwd):
    args = ['--include_untracked']
    result = validate_input(args)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_invalid_changelists_raises_exit(temp_cwd):
    args = ['--changelists_file', '  ']
    with pytest.raises(SystemExit):
        validate_input(args)


def test_validate_input_invalid_workspace_raises_exit(temp_cwd):
    args = ['--workspace_file', '  ']
    with pytest.raises(SystemExit):
        validate_input(args)


def test_validate_input_invalid_arg_raises_exit(temp_cwd):
    args = ['--unknown_arg']
    with pytest.raises(SystemExit):
        validate_input(args)
