import unittest
from app import create_app, db
from app.models import ServiceTicket, Member, Mechanic, Inventory
from datetime import datetime
from flask import jsonify, request


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()

        db.drop_all()
        db.create_all()

        @self.app.route("/tickets/", methods=["POST"])
        def create_ticket():
            data = request.get_json()
            ticket = ServiceTicket(description=data["description"])
            db.session.add(ticket)
            db.session.commit()
            return jsonify({"description": ticket.description}), 201


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_get_service_tickets(self):
        service_ticket_payload = {"descrption": "hello world!"}

        response = self.client.post("/", json=service_ticket_payload)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
