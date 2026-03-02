from app import create_app
from app.models import db, Mechanic 
from datetime import datetime
import unittest


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(name="test_user", email="test@email.com")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
        }

        response = self.client.post('/mechanic/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
    
    def test_get_mechanics(self):
        mechaic_payload = {
            "name": "John Doe",
            "DOB": "1900-01-01",
            "password": "123"
        }

        response = self.client.post('/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])


