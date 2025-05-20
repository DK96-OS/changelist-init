"""
"""
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree


def generate_sort_xml():
    """ Create the Sort.xml file in the Changelists directory.
    - Note: it is a hidden directory: .changelists/
    - This method may prompt the user for overwrite-confirmation when the sort.xml already contains something.
    """
    root = Element('sorting')
    tree = ElementTree(root)
    root.append(root_project_cl := Element('changelist'))
    root.append(test_cl := Element('changelist'))
    root_project_cl.set('name', 'Root Project')
    test_cl.set('name', 'Tests')
    if (output_file := Path(".changelist/sort.xml")).exists():
        if output_file.stat().st_size > 4:
            if not input("Sorting File Already Exists. Overwrite?").lower() in ('y',):
                return False
    else:
        output_file.touch()
    try:
        with open(output_file, "w") as f:
            tree.write(f, encoding='utf-8', xml_declaration=True)
        return True
    except BaseException:
        return False