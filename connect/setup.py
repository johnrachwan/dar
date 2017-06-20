import pyodbc
import json
import collections
import requests
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from distutils.core import setup
import py2exe
