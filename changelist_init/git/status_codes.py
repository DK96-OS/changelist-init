""" Managing Git Status Codes.
"""
from typing import Callable

from changelist_data.file_change import FileChange


def get_status_code_change_map(code) -> Callable[[str, ], FileChange]:
    """ Get a mapping callable for a specific code.
    """
    if code in ('M ', ' M', 'MM'):
        return lambda x: FileChange(before_path=x, before_dir=False, after_dir=False, after_path=x)
    if code in ('A ', ' A', 'AM', 'MA'):
        return lambda x: FileChange(after_dir=False, after_path=x)
    if code in ('D ', ' D', 'MD', 'DM'):
        return lambda x: FileChange(before_dir=False, before_path=x)
    if '?' in code or '!' in code:
        return lambda x: FileChange(after_dir=False, after_path=x)
    exit(f"Unknown Code: {code}")


#GIT_FILE_STATUS_CODES = ["M", "T", "A", "D", "R", "C"]

#def decode_status_code(
#    code_char: str
#) -> str | None:
#    """ Return the English Keyword describing the Status of the file, given the Code.
#    """
#    match code_char:
#        case 'M', 'U':
#            return "Updated"
#        case 'T':
#            return "TypeChange"
#        case 'A':
#            return "Added"
#        case 'D':
#            return "Deleted"
#        case 'R':
#            return "Renamed"
#        case 'C':
#            return "Copied"
#        case '?':
#            return "Untracked"
#        case '!':
#            return "Ignored"
#    return None
