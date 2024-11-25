""" Testing Main Package Merge File Changes method.
"""
import pytest

from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange

from changelist_init import merge_file_changes

from test.changelist_init.conftest import get_cl, fc_sample_list, get_fc_status, cl_sample_list, \
    create_sample_list_input


def test_merge_file_changes_empty_lists_returns_true():
    assert merge_file_changes([], [])


def test_merge_file_changes_empty_existing_list_returns_true():
    existing_list = []
    assert merge_file_changes(
        existing_list,
        [FileChange(after_path='hello.py', after_dir=False)]
    )
    assert len(existing_list) == 1


def test_merge_file_changes_empty_files_returns_true():
    existing_list = [Changelist('id', 'name', [])]
    assert merge_file_changes(
        existing_list,
        []
    )
    assert len(existing_list) == 1


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        [get_cl(cl_n, fc_sample_list(f_n * ' ' + get_fc_status(fc_status_n)))],
        [],
        [get_cl(cl_n, [])]
    ) for f_n in range(5) for cl_n in range(3) for fc_status_n in range(3)
])
def test_single_cl_containing_single_fc_merge_empty_returns_empty_cl(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, get_fc_status(fc_status_n))),
        [],
        [get_cl(cl_n, [])]
    ) for cl_n in range(3) for fc_status_n in range(3)
])
def test_single_cl_containing_multiple_fc_merge_empty_returns_empty_cl(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
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
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
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
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, get_fc_status(fc_status_n))),
        fc_sample_list(get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_single_fc_merge_single_unique_fc_returns_cl_new_fc(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, 3 * get_fc_status(fc_status_n))),
        fc_sample_list(4 * ' ' + get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(4 * ' ' + get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_three_fc_merge_single_unique_fc_returns_cl_new_fc(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, 3 * get_fc_status(fc_status_n))),
        fc_sample_list(2 * ' ' + get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(2 * ' ' + get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_three_fc_merge_single_existing_fc_returns_single_cl_single_fc(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(cl_n, 3 * get_fc_status(fc_status_n))),
        fc_sample_list(3 * get_fc_status(fc_status_i)),
        [get_cl(cl_n, fc_sample_list(3 * get_fc_status(fc_status_i)))]
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_single_cl_containing_three_fc_merge_all_existing_fc_returns_single_cl_all_fc(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(3, lambda x: x * ' ' + get_fc_status(fc_status_n))),
        fc_sample_list(3 * get_fc_status(fc_status_i)),
        cl_sample_list(create_sample_list_input(3, lambda x: x * ' ' + get_fc_status(fc_status_i))),
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_multi_cl_containing_three_fc_merge_all_existing_fc_returns_unchanged(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl


@pytest.mark.parametrize("existing_cl, files, expected_cl", [
    (
        cl_sample_list(create_sample_list_input(3, lambda x: x * ' ' + get_fc_status(fc_status_n))),
        fc_sample_list(3 * ' ' + 2 * get_fc_status(fc_status_i)),
        cl_sample_list(create_sample_list_input(3, lambda x: ((3 * ' ') + (2 * get_fc_status(fc_status_i))) if x == 0 else ' ')),
    ) for cl_n in range(3) for fc_status_n in range(3) for fc_status_i in range(3)
])
def test_multi_cl_containing_three_fc_merge_two_new_fc_returns_multi_cl_two_fc_in_first_cl(existing_cl, files, expected_cl):
    assert merge_file_changes(existing_cl, files)
    assert existing_cl == expected_cl
