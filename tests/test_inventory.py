from app import create_app
from app.models import db, Inventory 
from datetime import datetime
import unittest


class TestInventory(unittest.TestCase):
    def test_create_inventory(self):
        self.app = create_app('TestingConfig')
        self.inventory = Inventory(name="test_inventory", price='12')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.member)
            db.session.commit()
        self.client = self.app.test_client()
        self.assertEqual(response.json["name"], "test_inventory")
        self.assertEqual(response.json["price"], "12")

    def test_get_inventory(self):
        member_payload = {
            "name": "test_inventory",
            "price": "12",
        }

        response = self.client.post('/', json=member_payload)
        self.assertEqual(response.status_code, 201)
    
    def test_get_inventory_id(self):
        member_payload = {
            "name": "John Doe",
            "DOB": "1900-01-01",
            "password": "123"
        }

        response = self.client.post('/<int:inventory_id>/', json=member_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['id'], True)


    def test_update_inventory(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    
    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/members/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password!')
     
    
 
