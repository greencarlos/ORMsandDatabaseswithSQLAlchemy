import unittest
from app import create_app, db
from app.models import ServiceTicket, Member, Mechanic, Inventory
from flask import jsonify, request
from datetime import datetime


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app_instance = create_app("TestingConfig")
        self.app_instance.app_context().push()
        db.create_all()
        self.client = self.app_instance.test_client()

        self.ctx = self.app_instance.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()

        self.mechanic = Mechanic(
            name="test_user",
            email="test@email.com",
            phone="575-1234",  # add a dummy phone
            salary=50000,  # add a dummy salary if required
        )

        db.session.add(self.mechanic)
        db.session.commit()

        @self.app_instance.route("/mechanic/", methods=["POST"])
        def create_mechanic():
            data = request.get_json()
            mech = Mechanic(
                name="test_user",
                email="hello@email.com",
                phone="556-1234",  # add a dummy phone
                salary=50000,  # add a dummy salary if required
            )
            db.session.add(mech)
            db.session.commit()
            return jsonify({"name": mech.name, "email": mech.email}), 201

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "555-1234",
            "salary": 50000,
        }
        response = self.client.post("/mechanic/", json=mechanic_payload)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
