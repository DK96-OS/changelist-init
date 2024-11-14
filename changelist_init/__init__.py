""" Changelist Init Package.
"""
from itertools import groupby
from typing import Generator, Iterable

from changelist_data.changelist import Changelist
from changelist_data.file_change import FileChange

from changelist_init.git import get_status_lists
from changelist_init.git.git_file_status import GitFileStatus
from changelist_init.git.status_codes import get_status_code_change_map
from changelist_init.input import InputData


def initialize_file_changes(
    input_data: InputData,
) -> list[FileChange]:
    """ Get up-to-date File Change information in a list.
    """
    if input_data.include_untracked:
        file_status_generator = get_status_lists().merge_all()
    else:
        file_status_generator = get_status_lists().merge_tracked()
    return list(
        _map_file_status_to_changes(file_status_generator)
    )


def _map_file_status_to_changes(
    git_files: Iterable[GitFileStatus],
) -> Generator[FileChange, None, None]:
    """ Categorize by Status Code, and Map to FileChange data objects.

    Parameters:
    - git_files (Iterable[GitFileStatus]): An iterable or Generator providing GitFileStatus objects.

    Returns:
    FileChange - Yield by Generator.
    """
    for code, group in groupby(git_files, lambda w: w.code):
        mapper = get_status_code_change_map(code)
        for g in group:
            yield mapper(g.file_path)


def merge_file_changes(
    existing_lists: list[Changelist],
    files: list[FileChange],
) -> bool:
    """ Carefully Merge FileChange into Changelists.
    """
    if len(existing_lists) == 0:
        existing_lists.append(
            Changelist('12345678', "Initial Changelist", files, "", True)
        )
        return True
    # Validate files in existing lists
    for e_list in existing_lists:
        for c in e_list.changes:
            if c in files:
                files.remove(c)
            else:
                e_list.changes.remove(c)
    # Add the remaining new files
    existing_lists[0].changes.extend(files)
    return True
