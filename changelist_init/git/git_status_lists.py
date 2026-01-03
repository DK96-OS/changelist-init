""" Container for the Git Status Information.
 - Files are categorized into 4 lists.

**GitFileStatus NamedTuple Fields:**
 - code (str): The two character code describing the git file status.
 - file_path (str): The String path of the file, relative to repo directory.

**GitStatusLists NamedTuple Fields:**
 - staged (list): The list of staged GitFileStatus tuples.
 - unstaged (list): The list of unstaged GitFileStatus tuples.
 - partial_stage (list): The list of partially staged GitFileStatus tuples. Some changes are staged, some not.
 - untracked (list): The list of untracked GitFileStatus tuples.
"""
from collections import namedtuple
from typing import Generator

from changelist_init.git.git_tracking_status import GitTrackingStatus, from_str


GitFileStatus = namedtuple(
    'GitFileStatus',
    'code file_path',
)


GitStatusLists = namedtuple(
    'GitStatusLists',
    'staged unstaged partial_stage untracked',
)


def get_list(
    status_lists: GitStatusLists,
    tracking_status: GitTrackingStatus,
) -> list[GitFileStatus]:
    """ Obtain a List of File Status objects with the given Tracking Status.

**Parameters:**
 - status_lists (GitStatusLists): The collections of GitFileStatus objects.
 - tracking_status (GitTrackingStatus): The status group to obtain the list for.

**Returns:**
 list[GitFileStatus] - The specified list of GitFileStatus objects.
    """
    match tracking_status:
        case GitTrackingStatus.UNSTAGED:
            return status_lists.unstaged
        case GitTrackingStatus.STAGED:
            return status_lists.staged
        case GitTrackingStatus.PARTIAL_STAGE:
            return status_lists.partial_stage
    # Default: GitTrackingStatus.UNTRACKED
    return status_lists.untracked


def add_file_status(
    status_lists: GitStatusLists,
    file_status: GitFileStatus,
) -> bool:
    """ Add a File Status to the Lists.

**Parameters:**
 - status_lists (GitStatusLists): The collections of GitFileStatus objects.
 - file_status (GitFileStatus): The object containing status code and file.

**Returns:**
 bool - False if the file_status code was not able to be decoded.
    """
    if (tracking_status := from_str(file_status.code)) is None:
        return False
    get_list(status_lists, tracking_status).append(file_status)
    return True


def merge_all(
    status_lists: GitStatusLists,
    include_untracked: bool = True,
) -> Generator[GitFileStatus, None, None]:
    """ Combine all List contents into the Generator output, in this order: staged, partial, unstaged, untracked.

**Parameters:**
 - status_lists (GitStatusLists): The collections of GitFileStatus objects.
 - include_untracked (bool): Whether to include the untracked GitFileStatus objects in the generated output.

**Yields:**
 GitFileStatus - The GitFileStatus objects from the status_lists collection.
    """
    yield from status_lists.staged
    yield from status_lists.partial_stage
    yield from status_lists.unstaged
    if include_untracked:
        yield from status_lists.untracked
