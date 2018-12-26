from flask import Flask, request, redirect, jsonify
from uw_saml_helper import saml
from urllib.parse import urlparse
import os
app = Flask(__name__)

# ACS_URL = '/Shibboleth.sso/SAML2/POST'
ENTITY_ID = os.environ.get('ENTITY_ID')
ACS_URL = os.environ.get('ACS_URL')
ACS_PATH = urlparse(ACS_URL).path
UW_SAML = saml.SamlHandler(entity_id=ENTITY_ID, acs_url=ACS_URL,
                           request_class=saml.FlaskRequest)


@app.route("/login")
def hello():
    return redirect(UW_SAML.login_redirect_url(request))


@app.route(ACS_PATH, methods=['POST'])
def sso():
    return jsonify(UW_SAML.process_response(request))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
