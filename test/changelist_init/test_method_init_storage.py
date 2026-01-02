""" Testing CL-Init Package Method: init_storage
"""
import pytest
from changelist_data import Changelist

from changelist_init import init_storage
from test.changelist_init.conftest import construct_new_cl_data_storage


@pytest.mark.parametrize(
    'include_untracked, expected_file_count', [
        (False, 1),
        (True, 1),
    ]
)
def test_init_storage_single_staged_modify_repo(
    include_untracked,
    expected_file_count,
    single_staged_modify_repo
):
    init_storage(
        data_storage := construct_new_cl_data_storage(),
        include_untracked
    )
    assert len(result := data_storage.get_changelists()) == 1
    assert isinstance(result[0], Changelist)
    assert len(result[0].changes) == expected_file_count


@pytest.mark.parametrize(
    'include_untracked, expected_file_count', [
        (False, 1),
        (True, 3),
    ]
)
def test_init_storage_single_unstaged_plus_multi_files_in_new_dir_repo(
    include_untracked,
    expected_file_count,
    single_unstaged_plus_multi_files_in_new_dir_repo,
):
    init_storage(
        data_storage := construct_new_cl_data_storage(),
        include_untracked
    )
    assert len(result := data_storage.get_changelists()) == 1
    assert isinstance(result[0], Changelist)
    assert len(result[0].changes) == expected_file_count


@pytest.mark.parametrize(
    'include_untracked, expected_file_count', [
        (False, 1),
        (True, 3),
    ]
)
def test_init_storage_single_staged_modify_repo_plus_multi_files_in_new_dir_repo(
    include_untracked,
    expected_file_count,
    single_staged_modify_repo_plus_multi_files_in_new_dir_repo
):
    init_storage(
        data_storage := construct_new_cl_data_storage(),
        include_untracked
    )
    assert len(result := data_storage.get_changelists()) == 1
    assert isinstance(result[0], Changelist)
    assert len(result[0].changes) == expected_file_count
