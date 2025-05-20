""" Input Sub-Package Methods.
"""
from changelist_data import load_storage_from_file_arguments

from changelist_init import xml_generator
from changelist_init.input.argument_parser import parse_arguments
from changelist_init.input.input_data import InputData


def validate_input(
    arguments: list[str],
    verbose: bool = True,
) -> InputData:
    """ Parse and Validate the Arguments, and return Input Data.

**Parameters:**
 - arguments (list[str]): The arguments received by the program.
 - verbose (bool): Whether to print out affirmatory statements.

**Returns:**
 InputData - The InputData containing the program inputs. The other packages will process the data from here.
    """
    arg_data = parse_arguments(arguments)
    if arg_data.generate_sort_xml:
        if xml_generator.generate_sort_xml():
            if verbose:
                print("The file has been created: .changelists/sort.xml")
        else:
            print("Failed to create the sort.xml file.")
    return InputData(
        storage=load_storage_from_file_arguments(arg_data.changelists_file, arg_data.workspace_file),
        include_untracked=arg_data.include_untracked,
    )