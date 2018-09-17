from . import config
from collections import defaultdict
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
from onelogin.saml2.auth import OneLogin_Saml2_Auth


def login_redirect_url(request, request_class=DjangoRequest):
    pass


class SamlHandler(object):
    def __init__(self, sp=config.DefaultSp, idp=config.UwIdp):
        self.idp = idp()
        config = sp().to_dict()
        config.update(self.idp.to_dict())
        self.config = config

    def login_redirect_url(self, request):
        auth = OneLogin_Saml2_Auth(request.data, old_settings=self.config)
        return auth.login()

    def process_response(self, request):
        auth = OneLogin_Saml2_Auth(request.data, old_settings=self.config)
        auth.process_response()
        errors = auth.get_errors()
        if errors:
            raise Exception(auth.get_last_error_reason())
        return SamlResponse(attributes=auth.get_attributes(), idp=self.idp,
                            return_url=request.relay_state)


class RequestBase(object):
    data = {}
    relay_state = ''


class DjangoRequest(RequestBase):
    def __init__(self, request):
        self.data = {
            'https': 'on' if request.is_secure() else 'off',
            'http_host': request.META['HTTP_HOST'],
            'script_name': request.META['PATH_INFO'],
            'server_port': request.META['SERVER_PORT'],
            'post_data': request.POST.copy()
        }
        self.relay_state = request.POST.get('RelayState', '')


class FlaskRequest(RequestBase):
    def __init__(self, request):
        self.data = {
            'https': 'on' if request.scheme == 'https' else 'off',
            'http_host': request.host,
            'server_port': urlparse(request.url).port,
            'script_name': request.path,
            'get_data': request.args.copy(),
            'post_data': request.form.copy()
        }
        self.relay_state = request.form['RelayState']


class SamlResponse(object):
    username = None
    attributes = {}
    return_url = None

    def __init__(self, attributes, idp, return_url=None):
        self.return_url = return_url
        mapped_attributes = defaultdict(list)
        for key, value in attributes.items():
            if key == idp.id_attribute:
                self.username = value
            if key in idp.attribute_map:
                mapped_key = idp.attribute_map[key]
                if isinstance(mapped_key, config.ListAttribute):
                    mapped_attributes[mapped_key].append(value)
                else:
                    mapped_attributes[mapped_key] = value
            else:
                mapped_attributes[key].append(value)
        self.attributes = mapped_attributes
