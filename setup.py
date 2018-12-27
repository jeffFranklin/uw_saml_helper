import os
import re
from setuptools import setup, find_packages
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'VERSION')) as f:
    VERSION = f.readlines()[-1].strip()

with open(os.path.join(BASE_DIR, 'README.md')) as f:
      LONG_DESCRIPTION = f.read()

setup(name='uw-saml-helper',
      version=VERSION,
      url='https://github.com/UWIT-IAM/uw-saml-helper',
      author='UW-IT Identity and Access Management',
      author_email='help@uw.edu',
      description='UW SAML2 convenience package.',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      license='Apache License, Version 2.0',
      py_modules=['uw_saml_helper'],
      install_requires=['python3-saml']
      )