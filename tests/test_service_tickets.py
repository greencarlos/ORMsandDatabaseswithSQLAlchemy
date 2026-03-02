from app import create_app
from app.models import db, ServiceTicket 
from datetime import datetime
import unittest


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.service_ticket = ServiceTicket(description='hello world!')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.service_ticket)
            db.session.commit()
        self.client = self.app.test_client()

    def test_get_service_tickets(self):
        service_ticket_payload = {
            "descrption": "hello world!"
        }

        response = self.client.post('/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['description'], "hello world!")
    
