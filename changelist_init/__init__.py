""" CL-INIT Main Package Methods.
 Author: DK96-OS 2024 - 2025
"""
from typing import Iterable

from changelist_data import ChangelistDataStorage, StorageType
from changelist_data.changelist import Changelist, get_default_cl
from changelist_data.file_change import FileChange

from changelist_init import git, fc_to_cl_map
from changelist_init.input.input_data import InputData


_DEFAULT_CHANGELIST_ID = '4a74640f-90b3-86a1-ab28-af29299c84fd'
_DEFAULT_CHANGELIST_NAME = "Initial Changelist"


def process_cl_init(input_data: InputData):
    """ The Changelist Init Process.

**Parameters:**
 - input_data (InputData): The Changelist Init input data.
    """
    init_storage(
        storage=input_data.storage,
        include_untracked=input_data.include_untracked,
    )
    _write_storage(input_data.storage)


def merge_file_changes(
    existing_lists: list[Changelist],
    files: Iterable[FileChange],
):
    """ Merge FileChange into Changelists.
 - Leaves existing files in their Changelists.
 - Inserts all new files into the default Changelist.
 - Creates InitialChangelist with id:12345678 containing all files, if existing lists empty.

**Parameters:**
 - existing_lists (list[Changelist]): The list of Changelists that the InputData is starting with.
 - files (Iterable[FileChange]): The new FileChanges that have been obtained from Git.
    """
    if (default_cl := get_default_cl(existing_lists)) is not None:
        default_cl.changes.extend(
            fc_to_cl_map.merge_fc_generator(
                changelists=existing_lists,
                file_changes=files,
            )
        )
    else:
        existing_lists.append(
            Changelist(
                id=_DEFAULT_CHANGELIST_ID,
                name=_DEFAULT_CHANGELIST_NAME,
                changes=files if isinstance(files, list) else list(files),
                comment='',
                is_default=True,
            )
        )


def init_storage(
    storage: ChangelistDataStorage,
    include_untracked: bool,
):
    """ Get New FileChange Information, Merge into Changelists Data.

**Parameters:*
 - storage (ChangelistDataStorage): The Storage object to obtain existing CL from, and send updates to.
 - include_untracked (bool): Whether to tell git to include untracked files.

**Returns:**
 bool - True if the initialized data merged into Changelists Storage object successfully.
    """
    merge_file_changes(
        cl := storage.get_changelists(),
        git.generate_file_changes(include_untracked)
    )
    storage.update_changelists(cl)


def _write_storage(storage: ChangelistDataStorage) -> bool:
    if not storage.write_to_storage(): # Write Changelist Data file
        if storage.storage_type == StorageType.CHANGELISTS:
            exit("Failed to Write Changelist Data File!")
        elif storage.storage_type == StorageType.WORKSPACE:
            exit("Failed to Write Workspace Data File!")
    return True
