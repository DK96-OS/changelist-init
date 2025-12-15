""" Container for the Git Status Information.
    Files in Git Status are categorized into 3 groups.
    1. Staged
    2. Unstaged
    3. Untracked
    These three groups are stored in three lists in this data class.

**GitFileStatus NamedTuple Fields:**
 - code (str): The two character code describing the git file status.
 - file_path (str): The String path of the file, relative to repo directory.

**GitStatusLists NamedTuple Fields:**
 - untracked (list):
 - unstaged (list):
 - staged (list):
 - partial_stage (list):
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
    'untracked unstaged staged partial_stage',
)


def get_list(
    self: GitStatusLists,
    tracking_status: GitTrackingStatus,
) -> list[GitFileStatus]:
    """ Obtain a List of File Status objects with the given Tracking Status.
    """
    match tracking_status:
        case GitTrackingStatus.UNSTAGED:
            return self.unstaged
        case GitTrackingStatus.STAGED:
            return self.staged
        case GitTrackingStatus.PARTIAL_STAGE:
            return self.partial_stage
    # Default: GitTrackingStatus.UNTRACKED
    return self.untracked


def add_file_status(
    self: GitStatusLists,
    file_status: GitFileStatus,
) -> bool:
    """ Add A File Status to the Lists.
    """
    get_list(self, from_str(file_status.code)).append(file_status)
    return True


def merge_all(
    self: GitStatusLists,
    include_untracked: bool = True,
) -> Generator[GitFileStatus, None, None]:
    """ Combine all List contents into the Generator output, in this order: staged, partial, unstaged, untracked.
    """
    yield from self.staged
    yield from self.partial_stage
    yield from self.unstaged
    if include_untracked:
        yield from self.untracked
