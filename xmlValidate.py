
from lxml import etree


def validate_XML():
    """Validate an XML file represented as string. Follow all schemaLocations.
    :param xml: path to xml.
    :type xml: str
    """
    xml_file_new = r'C:\xmlvalidate\05983OUT.xml'

    xsd_file=r'C:\xmlvalidate\timingOutputSignals.xsd'
    xml_root = etree.parse(xml_file_new)
    xsd_root = etree.parse(xsd_file)
    schema = etree.XMLSchema(xsd_root)
    try:
        schema.validate(xml_root)
        schema.assertValid(xml_root)
    except etree.DocumentInvalid as e:
        print(e)

    print('Success!')


if __name__ == '__main__':
   validate_XML()
