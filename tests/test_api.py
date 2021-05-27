from app.view import *
from app.utils import *
from flask import json, jsonify
from unittest import TestCase
import unittest
from mock import patch, MagicMock

from server import app

flask_app = app


import requests

token = ""

def test_token_without_credentials_endpoint():
    with flask_app.test_client() as test_client:
        response = test_client.post('/token')
        assert response.status_code == 500

def test_token_correct_credentials_endpoint():
    with flask_app.test_client() as test_client:
        response = test_client.post('/token', data = {'secret_id': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9',
    'secret_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'})
        jsonData = json.loads(response.data)
        token = jsonData["data"]["token"]
        os.environ['TOKEN'] = token
        assert response.status_code == 200

def test_token_wrong_credentials_endpoint():
    with flask_app.test_client() as test_client:
        response = test_client.post('/token', data = {'secret_id': 'eyJhbGcijiJIUzI1NiIsInR5cCI6IkpXVCJ9',
    'secret_key': 'eyJhbGciOiJIUzI1NisInR5cCsI6IkpXVCJ9'})
        assert response.status_code == 500
