import time
import urllib2
import suds
import logging

from suds.client import Client
from suds.sax.text import Raw
from EntityConstructor import EntityConstructor

import xml.etree.ElementTree as ET
from lxml import etree


logging.basicConfig(level=logging.ERROR)
logging.getLogger('suds.client').setLevel(logging.INFO)


class TokenManager(object):
    @staticmethod
    def validate_user_token(token):
        return True


class HTTPSudsPreprocessor(urllib2.BaseHandler):
    def __init__(self, token):
        self.token = token

    def http_request(self, req):
        req.add_header('Authorization', "bearer " + str(self.token))
        return req


class PlatformConnector(object):
    TOKEN_TIMEOUT = 19 * 60  # Minutues * Seconds

    APPLICATION_KEY = "app.root.strevus.com"
    APPLICATION_SECRET = "c0Labor8"

    USER = "root@strevus.com"
    USER_PSWD = "c0Labor8"

    SERVICES = {'AUTH_SERVICE': "http://localhost:8081/strevus-platform-app/auth?wsdl",
                'DATA_SERVICE': "http://localhost:8081/strevus-platform-app/services/data?wsdl",
                'SYSTEM_SERVICE': "http://localhost:8081/strevus-platform-app/services/system?wsdl"}

    def __init__(self):
        self.token_time = None
        self.services_inited = False
        self.services = {}
        self.init_auth_service()
        self.user_session_token = self.request_token('user')
        self.transports = self.create_transports()
        self.init_services()

    def __getattribute__(self, item):
        attr = object.__getattribute__(self, item)
        if item == 'user_session_token' and self.services_inited:
            curr_time = time.time()
            if curr_time - self.token_time < PlatformConnector.TOKEN_TIMEOUT:
                return attr
            else:
                return self.request_token('user')
            # if not self.validate_user_token():
            #     return self.request_token('user')

        return attr

    # def validate_user_token(self):
    #     if not self.getUserByUsername(PlatformConnector.USER)['code']:
    #         return True
    #     else:
    #         return False

    def init_auth_service(self):
        self.services['AUTH_SERVICE'] = Client(PlatformConnector.SERVICES['AUTH_SERVICE'])

    def init_services(self):
        for service in PlatformConnector.SERVICES:
            if service == 'AUTH_SERVICE':
                continue
            else:
                self.services[service] = Client(PlatformConnector.SERVICES[service],
                                                transport=self.transports[service])

        self.services_inited = True

    def request_token(self, token_type):
        ip_xml = Raw('<ip>127.0.0.1</ip>')

        if token_type == 'user':
            self.token_time = time.time()
            return self.services['AUTH_SERVICE'].service.createToken1(ip_xml,
                                                                 PlatformConnector.APPLICATION_KEY,
                                                                 PlatformConnector.APPLICATION_SECRET,
                                                                 PlatformConnector.USER,
                                                                 PlatformConnector.USER_PSWD)['data']

    class HTTPSudsPreprocessor(urllib2.BaseHandler):
        def __init__(self, token):
            self.token = token

        def http_request(self, req):
            req.add_header('Authorization', "bearer " + str(self.token))
            return req

    def create_http_opener(self):
        return urllib2.build_opener(HTTPSudsPreprocessor(self.user_session_token))

    def create_transports(self):
        transports = {}

        opener = self.create_http_opener()

        for service in PlatformConnector.SERVICES:
            transports[service] = suds.transport.http.HttpTransport()
            if service != "AUTH_SERVICE":
                transports[service].urlopener = opener

        return transports

    # TODO Implement solution to update openers after token update.
    def update_openers(self):
        opener = self.create_http_opener()

        for service in PlatformConnector.SERVICES:
            if service != "AUTH_SERVICE":
                self.services[service].urlopener = opener

    def getUserByUsername(self, user_name):
        return self.services['SYSTEM_SERVICE'].service.getUserByUsername(user_name)

    def getOrganizationByLegalEntityKey(self, le_key):
        return self.services['SYSTEM_SERVICE'].service.getOrganizationByLegalEntityKey(le_key)

    def getFeedByName(self, name, id):
        return self.services['SYSTEM_SERVICE'].service.getFeedByName(name, id)

    def saveEntity(self, entity_xml):
        return self.services['DATA_SERVICE'].service.saveEntity(entity_xml)


pc = PlatformConnector()


# Main Flow

LE_KEY = "Entity:LegalEntity!Avox!Feed:Strevus"

# 02 Generate Object Key
resp1 = pc.getOrganizationByLegalEntityKey(LE_KEY)
print resp1
organization_id = resp1['id']

resp2 = pc.getFeedByName("AVOX", organization_id)
#print resp2
feed_id = resp2['id']

# 06 Save Entity
# we need feed id

e_xml = EntityConstructor().create_entity("outreach", feed_id)
#print etree.tostring(etree.fromstring(e_xml), pretty_print=True)

resp3 = pc.saveEntity(e_xml)
print resp3



# entity_params = pc.services['DATA_SERVICE'].factory.create('saveEntityParams')
# entity = pc.services['DATA_SERVICE'].factory.create('entity')
# le_key = pc.services['DATA_SERVICE'].factory.create('objectKey')
# le_key.value = "Entity:LegalEntityOutreach!!Feed:" + resp2['id']
# entity.key = le_key
# entity_params.entity = entity




# value_map = pc.services['DATA_SERVICE'].factory.create('adaptedMap')
# print value_map
#value_map['entry'].append({"legalEntityName":"dwed"})

#entity_params.entity.valueMap = value_map
#print entity_params



# resp3 = pc.saveEntity(entity_params)

# print resp3


#print pc.services['DATA_SERVICE'].wsdl['services'][0]['ports'][0]['binding']['operations']['saveEntity']

#print pc.services['DATA_SERVICE'].service.saveEntity(entity_params)

#print pc.services['DATA_SERVICE'].wsdl

#for method in pc.services['DATA_SERVICE'].wsdl.services[0].ports[0].methods.values():
#    print '%s(%s)' % (method.name, ', '.join('%s: %s' % (part.type, part.name) for part in method.soap.input.body.parts))


