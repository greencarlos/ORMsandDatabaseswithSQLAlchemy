import sys
import os

# Add the project root to the search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

import unittest
from flask import Flask, request, jsonify

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_sum(self):
        payload = {'num1': 2, 'num2': 3}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], 5)

    def sum():
        data = request.get_json()
        return jsonify({'result' : data['num1'] + data['num2']})

if __name__ == '__main__':
    unittest.main()
