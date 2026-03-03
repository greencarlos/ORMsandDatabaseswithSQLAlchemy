import unittest
from datetime import datetime
from app import create_app, db
from app.models import ServiceTicket, Member, Mechanic, Inventory
from flask import Flask, request, jsonify


class TestMember(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.member = Member(
            name="test_user",
            email="test@email.com",
            DOB=datetime.strptime("1900-01-01", "%Y-%m-%d").date(),
            password="test",
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.member)
            db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_member(self):
        member_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "DOB": "1900-01-01",
            "password": "123",
        }

        response = self.client.post("/members/", json=member_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "John Doe")

    def test_invalid_creation(self):
        member_payload = {"name": "John Doe", "DOB": "1900-01-01", "password": "123"}

        response = self.client.post("/members/", json=member_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["email"], ["Missing data for required field."])

    def test_login_member(self):
        credentials = {"email": "test@email.com", "password": "test"}

        response = self.client.post("/members/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        return response.json["token"]

    def test_invalid_login(self):
        credentials = {"email": "bad_email@emal.com", "password": "bad_pw"}

        response = self.client.post("/members/login", json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Invalid email or password")

    def test_get_all_members(self):
        response = self.client.get("/members/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], "test_user")

    def test_delete_member(self):
        headers = {"Authorization": "Bearer " + self.test_login_member()}
        response = self.client.delete("/members/", headers=headers)
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
