""" Git Management Package.
"""
from typing import Generator

from changelist_data.file_change import FileChange

from changelist_init.git import status_runner, status_reader, status_change_mapping
from changelist_init.git.git_status_lists import merge_all


def generate_file_changes(
    include_untracked: bool,
) -> Generator[FileChange, None, None]:
    """ Initialize FileChanges with a Generator.

**Parameters:**
 - include_untracked: Whether to include untracked files in the output.

**Yields:**
 FileChange - Those precious File Changes, created from Git Status output.
    """
    yield from status_change_mapping.map_file_status_to_changes(
        merge_all(
            status_lists=status_reader.read_git_status_output(
                status_runner.run_git_status(include_untracked)
            ),
            include_untracked=include_untracked,
        )
    )
