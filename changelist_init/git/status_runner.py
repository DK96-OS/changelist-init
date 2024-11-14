""" Runner for Git Status Operation
"""
import subprocess


def run_git_status() -> str:
    """ Run a Git Status Process and Return the Output.

    Returns:
    str - The output of the Git Status Operation.
    """
    result = subprocess.run(
        args=['git', 'status', '-s'],
        capture_output=True,
        text=True,
        universal_newlines=True,
        shell=False,
        timeout=5,
    )
    if (error := result.stderr) is not None and not len(error) < 1:
        exit(f"Git Status Runner Error: {error}")
    return result.stdout
