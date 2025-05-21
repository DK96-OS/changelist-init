#!/usr/bin/python
from sys import argv, path


def main(): # Have to import after appending parent dir to path
    import changelist_init
    input_data = changelist_init.input.validate_input(argv[1:])
    # Generate the Sorting Configuration file
    if input_data.generate_sort_xml:
        from changelist_init.xml_generator import generate_sort_xml
        if generate_sort_xml():
            print("The file has been created: .changelists/sort.xml")
        else:
            print("Failed to create the sort.xml file.")
    # Get New FileChange Information, Merge into Changelists Data
    if changelist_init.merge_file_changes(
        cl := input_data.storage.get_changelists(),
        changelist_init.git.generate_file_changes(input_data.include_untracked)
    ): # Successful Merge
        input_data.storage.update_changelists(cl)
        input_data.storage.write_to_storage()
    else:
        exit("Failed to Merge File Changes into Changelists")


if __name__ == "__main__":
    from pathlib import Path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    # Add the directory to sys.path
    path.append(str(current_directory))
    main()