""" Testing Input Init Package Method.
"""
from changelist_init.input import validate_input


def test_validate_input_():
    args = []
    result = validate_input(args)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_include_untracked_():
    args = ['--include_untracked']
    result = validate_input(args)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_invalid_changelists_raises_exit():
    args = ['--changelists_file', '  ']
    try:
        validate_input(args)
        raises_exit = False
    except SystemExit:
        raises_exit = True
    assert raises_exit


def test_validate_input_invalid_workspace_raises_exit():
    args = ['--workspace_file', '  ']
    try:
        validate_input(args)
        raises_exit = False
    except SystemExit:
        raises_exit = True
    assert raises_exit


def test_validate_input_invalid_arg_raises_exit():
    args = ['--unknown_arg']
    try:
        validate_input(args)
        raises_exit = False
    except SystemExit:
        raises_exit = True
    assert raises_exit
