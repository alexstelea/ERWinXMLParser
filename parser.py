__author__ = 'alexstelea'

import xml.etree.ElementTree as ET

tree = ET.parse('EDWSTDIC_orders_XSD.xsd')
root = tree.getroot()


def _recurse_xml_elements(node, depth=0):

    for child in node:
        depth += 1
        _recurse_xml_elements(child, depth=depth)

    if node.attrib:
        print str(node.attrib) + " Depth:" + str(depth)


def main():
    _recurse_xml_elements(root)


if __name__ == "__main__":
    main()