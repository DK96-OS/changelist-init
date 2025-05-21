""" Changelist Init Package.
"""
from typing import Iterable

from changelist_data.changelist import Changelist, get_default_cl
from changelist_data.file_change import FileChange

from changelist_init import git, fc_to_cl_map
from changelist_init.input.input_data import InputData


_DEFAULT_CHANGELIST_ID = '12345678'
_DEFAULT_CHANGELIST_NAME = "Initial Changelist"


def initialize_file_changes(
    input_data: InputData,
) -> list[FileChange]:
    """ Get up-to-date File Change information in a list.
 - Initializing Changelists begins by requesting File Information from Git.

**Parameters:**
 - input_data (InputData): ChangelistInit Input Package Data object, containing program input.

**Returns:**
 list[FileChange] - The List of File Changes, freshly squeezed from git.
    """
    return list(git.generate_file_changes(input_data.include_untracked))


def merge_file_changes(
    existing_lists: list[Changelist],
    files: Iterable[FileChange],
) -> bool:
    """ Carefully Merge FileChange into Changelists.
 - Inserts all files into the default Changelist.
 - Creates InitialChangelist with id:12345678 containing all files, if existing lists empty.

**Parameters:**
 - existing_lists (list[Changelist]): The list of Changelists that the InputData is starting with.
 - files (list[FileChange]): The new FileChanges that have been obtained from Git.

**Returns:**
 bool - True after the operation has finished.
    """
    if (default_cl := get_default_cl(existing_lists)) is not None:
        default_cl.changes.extend(
            fc_to_cl_map.merge_fc_generator(
                changelists=existing_lists,
                file_changes=files,
            )
        )
    else:
        existing_lists.append(Changelist(
            id=_DEFAULT_CHANGELIST_ID,
            name=_DEFAULT_CHANGELIST_NAME,
            changes=files if isinstance(files, list) else list(files),
            is_default=True,
        ))
    return True


def _get_default_cl(
    lists: list[Changelist],
) -> Changelist | None:
    """ Find the Default Changelist, or set the first Changelist to default.
        Returns None if lists is empty.
    """
    for cl in lists:
        if cl.is_default:
            return cl
    if len(lists) > 0: # First if no default attribute found
        return lists[0]
    return None