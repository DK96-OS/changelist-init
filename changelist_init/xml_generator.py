""" Module for creating the xml files.
"""
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree


def generate_sort_xml() -> bool:
    """ Create the Sort.xml file in the Changelists directory.
 - Note: it is a hidden directory: .changelists/
 - This method may prompt the user for overwrite-confirmation when the sort.xml already contains something.

**Returns:**
 bool - True if the write operation succeeded.
    """
    if (output_file := Path(".changelists/sort.xml")).exists():
        if output_file.stat().st_size > 4:
            if not input("Sorting File Already Exists. Overwrite?").lower() in ('y',):
                return False
    else:
        output_file.parent.mkdir(exist_ok=True)
        output_file.touch()
    sort_xml_tree = _prepare_initial_element_tree()
    try:
        with open(output_file, "x") as f:
            sort_xml_tree.write(f, encoding='utf-8', xml_declaration=True)
        return True
    except OSError:
        return False


def _prepare_initial_element_tree() -> ElementTree:
    """ The Initial Sort XML Tree:
 - Root Project Changelist
 - Tests Changelist

**Returns:**
 ElementTree - The XML ElementTree containing the Initial Changelists Config Information.
    """
    root = Element('sorting')
    root.append(root_project_cl := Element('changelist'))
    root.append(test_cl := Element('changelist'))
    root_project_cl.set('name', 'Root Project')
    test_cl.set('name', 'Tests')
    return ElementTree(root)