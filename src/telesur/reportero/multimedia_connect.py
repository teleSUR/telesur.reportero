import json
import httplib2
import hashlib
from urllib import urlencode

import zope.component

from plone.registry.interfaces import IRegistry
from plone.i18n.normalizer import idnormalizer

from telesur.reportero.controlpanel import IReporteroSettings

class MultimediaConnect(object):
    
    def __init__(self):
        registry = zope.component.getUtility(IRegistry)
        self.settings = registry.forInterface(IReporteroSettings)

    def firma_request(self, params_dict, key, secret):
        params_dict['key'] = key
        cadena = u'%s' % secret
        for name in sorted(params_dict.iterkeys()):
            cadena += u'%s%s' % (name, params_dict[name])
        return hashlib.md5(cadena).hexdigest()

    def multimedia_url(self):
        return self.settings.multimedia_url
    
    def upload_url(self):
        return self.settings.upload_url

    def security_key(self):
        return self.settings.security_key

    def key(self):
        return self.settings.key
    
    def normalize_data(self, data):
        DATA_KEYS = ['titulo', 'descripcion']
        result = {}
        for key in data.keys():
            if key in DATA_KEYS:
                result[key] = idnormalizer.normalize(data[key])
            else:
                result[key] = data[key]
        return result
    
    def create_structure(self, data, file_type):
        if file_type == "image":
            url = self.multimedia_url() + '/imagen/'
        else:
            url = self.multimedia_url() + '/clip/'
        body = self.normalize_data(data)
        headers = {'Accept': 'application/json'}
        key = self.security_key()
        sign_key = self.firma_request(body, self.key(), key)
        body['signature'] = sign_key
        http = httplib2.Http()
        response, content = http.request(url, 'POST', headers=headers, 
            body=urlencode(body))
        return response
    
    def get_structure(self, slug, file_type):
        if file_type == "image":
            url = self.multimedia_url() + '/imagen/' + slug
        else:
            url = self.multimedia_url() + '/clip/' + slug
        http = httplib2.Http()
        body = {}
        key = self.security_key()
        sign_key = self.firma_request(body, self.key(), key)
        body['signature'] = sign_key
        headers = {'Accept': 'application/json'}
        response, content = http.request(url, 'GET', headers=headers, 
                body=urlencode(body))
        content_json = json.loads(content)
        return response, content_json