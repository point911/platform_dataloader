# import lxml.etree as ET
# import lxml.builder as builder
#
# from lxml import objectify
#
#
# SCHEMA_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"
#
#
#
#
# entry_key_builder = builder.ElementMaker(namespace=SCHEMA_NAMESPACE,
#                                          nsmap={'xs': "http://www.w3.org/2001/XMLSchema"})
#
#
# graph = entry_key_builder.key(type="xs:string")
# #print(ET.tostring(graph, pretty_print=True))
#
#
#
#
# el = objectify.DataElement('5', _xsi='foo:string',
#                            nsmap={'foo': 'http://www.w3.org/2001/XMLSchema',
#                                    'myxsi': 'http://www.w3.org/2001/XMLSchema-instance'})
#
#
# print ET.tostring(el, pretty_print=True)


import xml.etree.ElementTree as ET
from collections import OrderedDict

SCHEMA_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"

entity_root = ET.Element("entity")

entity_key = ET.SubElement(entity_root, "key", {'xmlns:xsi': SCHEMA_NAMESPACE,
                                                'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
                                                'xsi:type': "xs:string"}, text="legalEntityName")
entity_key.text = "legalEntityName"

print ET.tostring(entity_root)

