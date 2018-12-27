from flask import Flask, request, redirect, jsonify
import uw_saml_helper
from urllib.parse import urlparse
import os

app = Flask(__name__)
ENTITY_ID = os.environ.get('ENTITY_ID')
ACS_URL = os.environ.get('ACS_URL')
ACS_PATH = urlparse(ACS_URL).path
uw_saml_helper.configure_sp(entity_id=ENTITY_ID, acs_url=ACS_URL)
UW_IDP = uw_saml_helper.UwIdp()


@app.route("/")
def hello():
    return redirect(UW_IDP.login_redirect())


@app.route(ACS_PATH, methods=['POST'])
def sso():
    return jsonify(UW_IDP.process_response(request.form))


if __name__ == '__main__':
    sslctx = ('/etc/ssl/certs/ssl-cert-snakeoil.pem', 
              '/etc/ssl/private/ssl-cert-snakeoil.key')
    app.run(host='0.0.0.0', ssl_context=sslctx, port=443, debug=True)
