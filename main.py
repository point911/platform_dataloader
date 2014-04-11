import urllib2
import suds
import logging
from suds.client import Client
from suds.sax.text import Raw


import xml.etree.ElementTree as ET
from lxml import etree


logging.basicConfig(level=logging.ERROR)
logging.getLogger('suds.client').setLevel(logging.INFO)


auth_service = "http://localhost:8081/strevus-platform-app/auth?wsdl"
data_service = "http://localhost:8081/strevus-platform-app/services/data?wsdl"
system_service = "http://localhost:8081/strevus-platform-app/services/system?wsdl"


# class PlatformConnector(object):
#     APPLICATION_KEY = "app.root.strevus.com"
#     APPLICATION_SECRET = "c0Labor8"
#
#     USER = "root@strevus.com"
#     USER_PSWD = "c0Labor8"
#
#     SERVICES = {'AUTH_SERVICE': "http://localhost:8081/strevus-platform-app/auth?wsdl",
#                 'DATA_SERVICE': "http://localhost:8081/strevus-platform-app/services/data?wsdl",
#                 'SYSTEM_SERVICE': "http://localhost:8081/strevus-platform-app/services/system?wsdl"}
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def get_opener_for_transport(auth_token):
#         return urllib2.build_opener(HTTPSudsPreprocessor(auth_token))
#
#
#     def request_token(self, token_type):
#         ip_xml = Raw('<ip>127.0.0.1</ip>')
#
#         if token_type == 'user':
#             return auth_service_client.service.createToken1(ip_xml, key, secret, user, user_pswd)
#
#     def validate_token(self):
#         pass


class HTTPSudsPreprocessor(urllib2.BaseHandler):
    def __init__(self, token):
        self.token = token

    def http_request(self, req):
        req.add_header('Authorization', "bearer " + str(self.token))
        return req


def create_entity_xml(entity_name, user_name):
    SCHEMA_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"

    entity_prefix = "Entity:LegalEntity!!User:"

    entity_root = ET.Element("entity")

    child_map = ET.SubElement(entity_root, "childMap")

    value_map = ET.SubElement(entity_root, "valueMap")

    entry = ET.SubElement(value_map, "entry")

    entry_key_attrs = {'xmlns:xsi': SCHEMA_NAMESPACE,
                       'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
                       'xsi:type': "xs:string"}
    entry_key = ET.SubElement(entry, "key", entry_key_attrs)
    entry_key.text = "legalEntityName"

    entry_value_attrs = {'xmlns:xsi': SCHEMA_NAMESPACE,
                         'xmlns:ns3': "http://client.platform.services.http.transport.strevus.com/",
                         'xsi:type': 'ns3:value'}
    entry_value = ET.SubElement(entry, "value", entry_value_attrs)

    entry_value_attr_name = ET.SubElement(entry_value, "name")
    entry_value_attr_name.text = "legalEntityName"

    entry_value_timestamp = ET.SubElement(entry_value, "timestamp")
    entry_value_timestamp.text = "1396283924076"

    entry_value_attr_value = ET.SubElement(entry_value, "value")
    entry_value_attr_value.text = "String[{}]".format(entity_name)

    key = ET.SubElement(entity_root, "key")
    key_value = ET.SubElement(key, "value")
    key_value.text = entity_prefix + user_name

    el_entity_xml = ET.tostring(entity_root)
    el_entity_xml = Raw(el_entity_xml)

    return el_entity_xml


def create_entity_suds(skeleton, i_set):
    skeleton['key'] = "Entity:LegalEntity!!User:"+i_set
    skeleton['valueMap']['entry'] = {"name": "legalEntityName"}

    entity_suds = skeleton
    return entity_suds


def get_entity_xml(identity_set):
    entityRef_root = ET.Element("entityRef")
    objectSubtype = ET.SubElement(entityRef_root, "objectSubtype")
    objectSubtype.text = "LegalEntity"
    objectType = ET.SubElement(entityRef_root, "objectType")
    objectType.text = "Entity"
    entityRef_xml_str = ET.tostring(entityRef_root, encoding='utf-8', method='xml')

    objectKey_root = ET.Element("objectKey")
    value = ET.SubElement(objectKey_root, "value")
    value.text = identity_set
    objectKey_xml_str = ET.tostring(objectKey_root, encoding='utf-8', method='xml')

    return Raw("".join([entityRef_xml_str, objectKey_xml_str]))


def get_user_id_by_name(user_name):
    pass


key = "app.root.strevus.com"
secret = "c0Labor8"

user = "root@strevus.com"
user_pswd = "c0Labor8"

auth_service_client = Client(auth_service)

ip_xml = Raw('<ip>127.0.0.1</ip>')
token = auth_service_client.service.createToken1(ip_xml, key, secret, user, user_pswd)

opener = urllib2.build_opener(HTTPSudsPreprocessor(token['data']))


system_service_transport = suds.transport.http.HttpTransport()
system_service_transport.urlopener = opener


data_service_transport = suds.transport.http.HttpTransport()
data_service_transport.urlopener = opener

system_service_client = suds.client.Client(system_service, transport=system_service_transport)
get_user_response = system_service_client.service.getUserByUsername(user)
user_id = get_user_response['data']['id']

entity_xml = create_entity_xml("SUL AMERICA S A", user_id)
print etree.tostring(etree.fromstring(entity_xml), pretty_print=True)


data_service_client = suds.client.Client(data_service, transport=data_service_transport)
#ent = data_service_client.factory.create("entity")
#new_entity = create_entity_suds(ent, user_id)
#print new_entity


resp3 = data_service_client.service.saveEntity(entity_xml)
#print resp3



i_set_resp = str(resp3['identitySetKey']['value'])
i_set = "!".join(str(resp3['identitySetKey']['value']).split("!")[0:-1])
#print i_set

get_entity_request = get_entity_xml(i_set_resp)

resp4 = data_service_client.service.getEntity(get_entity_request)


new_ent = resp4['entity']


new_ent['key'] = "Entity:LegalEntity!!User:ffffb8d799c76d70848eb8e8563116d8"

print new_ent






#resp5 = data_service_client.service.saveEntity(new_ent)
#print resp5








########## FREEMIUM DATALOADER PHASE

# client_1 = suds.client.Client(url1, transport=http1)
#
# entity_id = "IdentitySet:Entity:LegalEntity!freemium!Feed:Strevus"
#
# entity_id_xml = Raw("<objectKey>" + entity_id + "</objectKey>")
#
# arg1 = "<entityRef><objectSubtype>LegalEntity</objectSubtype><objectType>Entity</objectType></entityRef><objectKey><value>IdentitySet:Entity:LegalEntity!10168354!Application:ffffb4cbf17da170857db8e8563116d8</value></objectKey>"
# arg1_xml = Raw(arg1)
#
# resp2 = client_1.service.getEntity(arg1_xml)
#
# print resp2
# lr = client_1.last_received()
# print lr



# client_2 = suds.client.Client(url2, transport=http)
#
# resp = client_2.service.getOrganizationByLegalEntityKey("IdentitySet:Entity:LegalEntity!freemium!Feed:Strevus")
#
# print resp
#
# resp1 = client_2.service.getRoleByName("ROLE_FREEMIUM_USER", resp['id'])
#
# print resp1
