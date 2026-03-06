from app import create_app, db
from app.models import ServiceTicket, Member, Mechanic, Inventory
from flask import jsonify, request
from datetime import datetime
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app_instance = create_app("TestingConfig")
        self.client = self.app_instance.test_client()
        self.ctx = self.app_instance.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

        @self.app_instance.route("/inventory", methods=["POST"])
        def create_inventory():
            data = request.get_json()
            inv = Inventory(name=data["name"], price=data["price"])
            db.session.add(inv)
            db.session.commit()
            return jsonify({"name": inv.name, "price": inv.price}), 201


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_inventory(self):
        payload = {"name": "test_inventory", "price": "12"}
        response = self.client.post("/inventory", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["name"], "test_inventory")
        self.assertEqual(data["price"], 12.0)


if __name__ == "__main__":
    unittest.main()
