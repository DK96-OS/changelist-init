""" Testing Main Package Merge File Changes method.
"""
import pytest
from changelist_data.changelist import Changelist
from changelist_data.file_change import create_fc

from changelist_init.data import merge_file_changes, _DEFAULT_CHANGELIST_NAME, _DEFAULT_CHANGELIST_ID
from test.changelist_init.conftest import get_cl, fc_sample_list, get_fc_status, cl_sample_list, \
    create_sample_list_input, construct_new_cl_data_storage, _SAMPLE_FC_0


def test_merge_file_changes_empty_storage_no_fc_creates_default_cl():
    storage = construct_new_cl_data_storage()
    merge_file_changes(storage, [])
    result = storage.get_changelists()
    assert len(result) == 1
    default_cl = result[0]
    assert default_cl.id == _DEFAULT_CHANGELIST_ID
    assert default_cl.name == _DEFAULT_CHANGELIST_NAME
    assert default_cl.changes == []
    assert default_cl.comment == ''
    assert default_cl.is_default


def test_merge_file_changes_empty_storage_sample_fc_0_adds_to_default_cl():
    storage = construct_new_cl_data_storage()
    test_input = [create_fc(_SAMPLE_FC_0)]
    merge_file_changes(storage, test_input)
    result = storage.get_changelists()
    assert len(result) == 1
    default_cl = result[0]
    assert default_cl.id == _DEFAULT_CHANGELIST_ID
    assert default_cl.name == _DEFAULT_CHANGELIST_NAME
    assert default_cl.changes == test_input
    assert default_cl.comment == ''
    assert default_cl.is_default


def test_merge_file_changes_default_cl_in_storage_no_fc_clears_default_cl_fc():
    storage = construct_new_cl_data_storage()
    storage.update_changelists(
        [Changelist(_DEFAULT_CHANGELIST_ID, _DEFAULT_CHANGELIST_NAME, [], '', True)]
    )
    merge_file_changes(storage, [])
    result = storage.get_changelists()
    assert len(result) == 1
    # Default CL is present
    default_cl = result[0]
    assert len(default_cl.changes) == 0


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        [get_cl(cl_n, fc_sample_list(f_n * ' ' + get_fc_status(fc_status_n)))],
        [],
        [get_cl(cl_n, [])]
    ) for f_n in range(5) for cl_n in range(3) for fc_status_n in range(3)
])
def test_single_cl_containing_single_fc_merge_empty_returns_empty_cl(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, get_fc_status(fc_status_n))),
        [],
        [get_cl(cl_n, [])]
    ) for cl_n in range(3) for fc_status_n in range(3)
])
def test_single_cl_containing_multiple_fc_merge_empty_returns_empty_cl(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list([
            get_fc_status(fc_status_n),
            ' ' + get_fc_status(fc_status_n),
            '  ' + get_fc_status(fc_status_n),
        ]),
        [],
        [
            get_cl(0, []),
            get_cl(1, []),
            get_cl(2, []),
        ]
    ) for fc_status_n in range(3)
])
def test_multi_cl_containing_single_unique_fc_merge_empty_returns_empty_cls(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list([
            get_fc_status(fc_status_n),
            ' ' + get_fc_status(fc_status_n),
            '  ' + get_fc_status(fc_status_n),
        ]),
        [],
        [
            get_cl(0, []),
            get_cl(1, []),
            get_cl(2, []),
        ]
    ) for cl_n in range(3) for fc_status_n in range(3)
])
def test_multi_cl_containing_single_same_fc_merge_empty_returns_empty_cls(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, get_fc_status(fc_status_n))),
        fc_sample_list(get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_single_fc_merge_single_unique_fc_returns_cl_new_fc(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, 3 * get_fc_status(fc_status_n))),
        fc_sample_list(4 * ' ' + get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(4 * ' ' + get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_three_fc_merge_single_unique_fc_returns_cl_new_fc(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, 3 * get_fc_status(fc_status_n))),
        fc_sample_list(2 * ' ' + get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(2 * ' ' + get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_three_fc_merge_single_existing_fc_returns_single_cl_single_fc(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, 3 * get_fc_status(fc_status_n))),
        fc_sample_list(3 * get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(3 * get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_three_fc_merge_all_existing_fc_returns_single_cl_all_fc(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(3, lambda x: x * ' ' + get_fc_status(fc_status_n))),
        fc_sample_list(3 * get_fc_status(fc_status_i)),
        cl_sample_list(create_sample_list_input(3, lambda x: x * ' ' + get_fc_status(fc_status_i))),
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_multi_cl_containing_three_fc_merge_all_existing_fc_returns_unchanged(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl


@pytest.mark.parametrize(
    "existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(3, lambda x: x * ' ' + get_fc_status(fc_status_n))),
        fc_sample_list(3 * ' ' + 2 * get_fc_status(fc_status_i)),
        cl_sample_list(create_sample_list_input(3, lambda x: ((3 * ' ') + (2 * get_fc_status(fc_status_i))) if x == 0 else ' ')),
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_multi_cl_containing_three_fc_merge_two_new_fc_returns_multi_cl_two_fc_in_first_cl(existing_cl, files, expected_cl):
    storage = construct_new_cl_data_storage()
    storage.update_changelists(existing_cl)
    #
    merge_file_changes(storage, files)
    result = storage.get_changelists()
    assert result == expected_cl
