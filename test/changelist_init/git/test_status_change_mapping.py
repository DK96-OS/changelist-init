""" Testing Status Change Mapping Method.
"""
import pytest
from changelist_data import file_change

from changelist_init.git.status_change_mapping import get_status_code_change_map


@pytest.mark.parametrize(
    'status_code', [
        'A ',
        ' A',
        'AM',
        'MA',
    ]
)
def test_get_status_code_change_map_create_inputs_returns_create_fc(status_code):
    assert file_change.create_fc == get_status_code_change_map(status_code)


@pytest.mark.parametrize(
    'status_code', [
        'M ',
        ' M',
        'MM',
        'MM',
    ]
)
def test_get_status_code_change_map_update_inputs_returns_update_fc(status_code):
    assert file_change.update_fc == get_status_code_change_map(status_code)


@pytest.mark.parametrize(
    'status_code', [
        'D ',
        ' D',
        'DM',
        'MD',
    ]
)
def test_get_status_code_change_map_delete_inputs_returns_delete_fc(status_code):
    assert file_change.delete_fc == get_status_code_change_map(status_code)


@pytest.mark.parametrize(
    'status_code', [
        '??',
        '!!',
    ]
)
def test_get_status_code_change_map_untracked_inputs_returns_create_fc(status_code):
    assert file_change.create_fc == get_status_code_change_map(status_code)


@pytest.mark.parametrize(
    'status_code', [
        'C ',  # Copied
        ' C',
        'R ',  # Renamed
        ' R',
        'T ',  # File Type
        ' T',
        'U ',  # Unmerged
        ' U',
    ]
)
def test_get_status_code_change_map_unsupported_codes_returns_none(status_code):
    assert get_status_code_change_map(status_code) is None
