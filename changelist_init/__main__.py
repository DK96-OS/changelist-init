#!/usr/bin/python


def main(): # Have to import after appending parent dir to path
    from sys import argv
    from changelist_init.input import validate_input
    input_data = validate_input(argv[1:])
    # Generate FileChange info from git, update ChangelistDataStorage object.
    from changelist_init import init_storage
    if not init_storage(
        storage=input_data.storage,
        include_untracked=input_data.include_untracked,
    ):
        exit("Failed to Merge new FileChanges into Changelists.")
    # Write Changelist Data file
    if not input_data.storage.write_to_storage():
        exit("Failed to Write Changelist Data File!")


if __name__ == "__main__":
    from pathlib import Path
    from sys import path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    # Add the directory to sys.path
    path.append(str(current_directory))
    main()
