FROM python:3

RUN apt-get update && \
    apt-get install -y libxmlsec1-dev && \
    apt-get clean

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY uw_saml_helper .
EXPOSE 80
ENV FLASK_APP=app
ENV FLASK_DEBUG=1
ENV ENTITY_ID=https://docker.internal/shibboleth
ENV ACS_URL=https://docker.internal/Shibboleth.sso/SAML2/POST

# CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]

CMD ["python", "app.py"]
