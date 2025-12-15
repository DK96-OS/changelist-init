""" Git Tracking Status Enum.
"""
from enum import auto, IntEnum


class GitTrackingStatus(IntEnum):
    UNTRACKED = auto()
    UNSTAGED = auto()
    STAGED = auto()
    PARTIAL_STAGE = auto()


def from_str(
    status_code_str: str,
) -> GitTrackingStatus:
    """ Obtain the Tracking Status of the given Status code str.

**Parameters:**
 - status_code_str (str): A 2 char status code from git.

**Returns:**
 GitTrackingStatus - The Tracking Status Enum for the given Status Code.
    """
    if len(code := status_code_str) != 2:
        raise ValueError("Status Code must be length 2.")
    match code:
        case '??':
            return GitTrackingStatus.UNTRACKED
    if code.startswith(' '):
        return GitTrackingStatus.UNSTAGED
    if code.endswith(' '):
        return GitTrackingStatus.STAGED
    # If both code points are non-empty, is partially_staged
    return GitTrackingStatus.PARTIAL_STAGE
