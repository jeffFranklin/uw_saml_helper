from uw_saml_helper.config import SpConfig, UwIdp, ListAttribute
from collections import defaultdict
from urllib.parse import urlparse
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from logging import getLogger
logger = getLogger(__name__)


class SamlHandler(object):
    def __init__(self, sp=None, idp=None, request_class=None):
        if not sp:
            sp = SpConfig()
        self.idp = idp or UwIdp()
        self.request_class = request_class or DjangoRequest
        config = sp.to_dict()
        config.update(self.idp.to_dict())
        self.config = config

    def login_redirect_url(self, request):
        request = self.request_class(request)
        print(f'request.data={request.data}')
        auth = OneLogin_Saml2_Auth(request.data, old_settings=self.config)
        return auth.login()

    def process_response(self, request):
        request = self.request_class(request)
        auth = OneLogin_Saml2_Auth(request.data, old_settings=self.config)
        auth.process_response()
        errors = auth.get_errors()
        if errors:
            raise Exception(auth.get_last_error_reason())
        attributes = auth.get_attributes()
        response = SamlResponse(attributes=attributes, idp=self.idp,
                                return_url=request.relay_state)
        return vars(response)


class RequestBase(object):
    data = {}
    relay_state = ''


class DjangoRequest(RequestBase):
    def __init__(self, request):
        self.data = {
            'https': 'on',
            'http_host': request.META['HTTP_HOST'],
            'script_name': request.META['PATH_INFO'],
            'server_port': request.META['SERVER_PORT'],
            'post_data': request.POST.copy()
        }
        self.relay_state = request.POST.get('RelayState', '')


class FlaskRequest(RequestBase):
    def __init__(self, request):
        self.data = {
            'https': 'on',
            'http_host': request.host,
            'server_port': urlparse(request.url).port,
            'script_name': request.path,
            'get_data': request.args.copy(),
            'post_data': request.form.copy()
        }
        self.relay_state = request.form.get('RelayState', '')


class SamlResponse(object):
    username = None
    attributes = {}
    return_url = None

    def __init__(self, attributes, idp, return_url=None):
        self.return_url = return_url
        mapped_attributes = defaultdict(list)
        for key, values in attributes.items():
            if key == idp.id_attribute and values:
                self.username = values[0]
            if key in idp.attribute_map:
                mapped_key = idp.attribute_map[key]
                if isinstance(mapped_key, ListAttribute):
                    mapped_attributes[mapped_key].extend(values)
                elif values:
                    mapped_attributes[mapped_key] = values[0]
            else:
                mapped_attributes[key].extend(values)
        self.attributes = mapped_attributes

