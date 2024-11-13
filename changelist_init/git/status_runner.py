""" Runner for Git Status Operation
"""
import subprocess


def run_git_status() -> str:
    """ Run a Git Status Process and Return the Output.

    Returns:
    str - The output of the Git Status Operation.
    """
    result = subprocess.run(
        args=['git status -s'],
        capture_output=True,
        text=True,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
        timeout=5,
    )
    #error = result.stderr
    return result.stdout
