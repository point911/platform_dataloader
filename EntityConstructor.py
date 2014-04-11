import json
from lxml import etree
import time
import uuid
import xml.etree.ElementTree as ET
from suds.sax.text import Raw
from random_value_generator import get_random


class EntityConstructor(object):

    SCHEMA_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"

    XML_SCHEMA_INSTANCE = {'xmlns:xsi': SCHEMA_NAMESPACE}

    XML_SCHEMA = {'xmlns:xs': "http://www.w3.org/2001/XMLSchema"}
    XML_NAMESPACE = {'xmlns:ns3': "http://client.platform.services.http.transport.strevus.com/"}

    KEY_ATTRS = dict(XML_SCHEMA_INSTANCE.items() + XML_SCHEMA.items())
    VALUE_ATTRS = dict(XML_SCHEMA_INSTANCE.items() + XML_NAMESPACE.items())

    OUTREACH_LE_PREFIX = "Entity:LegalEntityOutreach!!Feed:"

    def __init__(self):
        self.le_outreach_template = self.load_template("outreach")

    @staticmethod
    def load_template(template_type):
        if template_type == "outreach":
            file_path = "./le_outreach_template.json"
        else:
            raise NameError

        json_template = open(file_path).read()
        template = json.loads(json_template)
        return template

    def create_entity(self, entity_type, feed_id):
        if entity_type == "outreach":
            return self.create_entity_outreach(feed_id)

    def create_entity_outreach(self, feed_id):
        entity_root = ET.Element("entity")

        for key in self.le_outreach_template:
            le_part = self.create_le_part(key, feed_id)
            entity_root.append(le_part)

        le_entity = ET.tostring(entity_root)
        el_entity_xml = Raw(le_entity)

        return el_entity_xml

    def create_le_part(self, key, feed_id):
        if key == "childMap":
            le_part = self.create_outreach_le_childmap()
        elif key == "key":
            le_part = self.create_outreach_le_key(feed_id)
        elif key == "valueMap":
            le_part = self.create_outreach_le_valuemap()
        else:
            raise AttributeError

        return le_part

    def create_outreach_le_key(self, feed_id):
        key = ET.Element("key")
        key_value = ET.SubElement(key, "value")
        key_value.text = EntityConstructor.OUTREACH_LE_PREFIX + feed_id

        return key

    def create_outreach_le_valuemap(self):
        value_map = ET.Element("valueMap")

        value_map_template = self.le_outreach_template['valueMap']

        for key in value_map_template:
            value = get_random(key, "String")
            value_map_part = EntityConstructor.create_value_map_entry_1(key, value)

            value_map.append(value_map_part)

        return value_map

    @staticmethod
    def create_value_map_entry_1(key_name, value):
        entry = ET.Element("entry")

        key_xsi_type = {'xsi:type': "xs:string"}
        value_xsi_type = {'xsi:type': 'ns3:value'}

        entry_key_attrs = EntityConstructor.KEY_ATTRS
        entry_key_attrs.update(key_xsi_type)

        entry_value_attrs = EntityConstructor.VALUE_ATTRS
        entry_value_attrs.update(value_xsi_type)

        entry_key = ET.SubElement(entry, "key", entry_key_attrs)
        entry_key.text = key_name

        entry_value = ET.SubElement(entry, "value", entry_value_attrs)

        entry_value_attr_name = ET.SubElement(entry_value, "name")
        entry_value_attr_name.text = key_name

        entry_value_timestamp = ET.SubElement(entry_value, "timestamp")
        entry_value_timestamp.text = str(int(time.time()))

        entry_value_attr_value = ET.SubElement(entry_value, "value")
        entry_value_attr_value.text = value

        return entry

    def create_outreach_le_childmap(self):
        child_map = ET.Element("childMap")
        child_map_template = self.le_outreach_template['childMap']

        for child in child_map_template:
            new_child = self.create_child(child)
            child_map.append(new_child)

        return child_map

    def create_child(self, child_key_name):
        child_uuid = uuid.uuid4().hex

        child_template = self.le_outreach_template['childMap'][child_key_name]
        child_root = ET.Element("entry")

        child_key = self.create_child_key(child_key_name, child_uuid)
        child_root.append(child_key)

        child_value = self.create_child_value(child_key_name, child_template['value'], child_uuid)
        child_root.append(child_value)

        return child_root

    @staticmethod
    def create_child_key(child_name, child_uuid):
        child_key_xsi_type = {"xsi:type": "ns3:childKey"}
        child_key_attrs = EntityConstructor.VALUE_ATTRS
        child_key_attrs.update(child_key_xsi_type)

        child_key = ET.Element("key", child_key_attrs)
        child_key_value = ET.SubElement(child_key, "value")
        child_key_value.text = child_name + "!" + child_uuid

        return child_key

    @staticmethod
    def create_child_value(child_key_name, child_template, child_uuid):
        child_value_xsi_type = {"xsi:type": "ns3:childRecord"}
        child_value_attrs = EntityConstructor.VALUE_ATTRS
        child_value_attrs.update(child_value_xsi_type)

        child_value = ET.Element("value", child_value_attrs)

        for key in child_template:

            sub_child_value = ET.Element(key)
            if key == "childMap":
                pass
            elif key == "deleted":
                sub_child_value.text = "false"
            elif key == "key":
                sub_child_value_key = ET.SubElement(sub_child_value, "value")
                sub_child_value_key.text = child_key_name + "!" + child_uuid
            elif key == "valueMap":
                for value_map_entry_name, value_map_entry_value in child_template['valueMap'].iteritems():
                    sub_entry = EntityConstructor.create_child_value_map_entry(value_map_entry_name,)
                    sub_child_value.append(sub_entry)

            child_value.append(sub_child_value)

        return child_value

    @staticmethod
    def create_child_value_map_entry(key_name):
        entry = ET.Element("entry")

        key_xsi_type = {'xsi:type': "xs:string"}
        entry_key_attrs = EntityConstructor.XML_SCHEMA
        entry_key_attrs.update(key_xsi_type)

        entry_key = ET.SubElement(entry, "key", entry_key_attrs)
        entry_key.text = key_name

        entry_value_attrs = {"xsi:type": "ns3:value"}
        entry_value = ET.SubElement(entry, "value", entry_value_attrs)

        entry_value_attr_name = ET.SubElement(entry_value, "name")
        entry_value_attr_name.text = key_name

        entry_value_timestamp = ET.SubElement(entry_value, "timestamp")
        entry_value_timestamp.text = str(int(time.time()))

        entry_value_attr_value = ET.SubElement(entry_value, "value")
        entry_value_attr_value.text = get_random(key_name, "String")

        return entry





    @staticmethod
    def create_entity_xml(entity_name, feed_id):
        entity_prefix = "Entity:LegalEntityOutreach!!Feed:"

        entity_root = ET.Element("entity")

        child_map = ET.SubElement(entity_root, "childMap")

        value_map = ET.SubElement(entity_root, "valueMap")

        value_map.append(EntityConstructor.create_value_map_entry("tradingStatus", "String[ACTIVE]"))
        value_map.append(EntityConstructor.create_value_map_entry("riskLevel", "String[low]"))
        value_map.append(EntityConstructor.create_value_map_entry("legalEntityName", "String[{}]".format(entity_name)))

        key = ET.SubElement(entity_root, "key")
        key_value = ET.SubElement(key, "value")
        key_value.text = entity_prefix + feed_id

        el_entity_xml = ET.tostring(entity_root)
        el_entity_xml = Raw(el_entity_xml)

        return el_entity_xml


    @staticmethod
    def create_value_map_entry(key_name, value):
        entry = ET.Element("entry")


        entry_key_attrs = {'xmlns:xsi': EntityConstructor.SCHEMA_NAMESPACE,
                           'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
                           'xsi:type': "xs:string"}

        entry_key = ET.SubElement(entry, "key", entry_key_attrs)
        entry_key.text = key_name

        entry_value_attrs = {'xmlns:xsi': EntityConstructor.SCHEMA_NAMESPACE,
                             'xmlns:ns3': "http://client.platform.services.http.transport.strevus.com/",
                             'xsi:type': 'ns3:value'}

        entry_value = ET.SubElement(entry, "value", entry_value_attrs)

        entry_value_attr_name = ET.SubElement(entry_value, "name")
        entry_value_attr_name.text = key_name

        entry_value_timestamp = ET.SubElement(entry_value, "timestamp")
        entry_value_timestamp.text = str(int(time.time()))

        entry_value_attr_value = ET.SubElement(entry_value, "value")
        entry_value_attr_value.text = value

        return entry



e = EntityConstructor()
#pprint(e.le_outreach_template)

le_xml = e.create_entity("outreach", "feedid")
print etree.tostring(etree.fromstring(le_xml), pretty_print=True)