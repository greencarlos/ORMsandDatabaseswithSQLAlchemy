from .schemas import member_schema, members_schema, login_schema
from app.blueprints.service_tickets import service_tickets_schema  
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from marshmallow import ValidationError
from datetime import date
from app.models import Member, ServiceTickets, db
from app.extensions import limiter, cache, ma
from app.utils.util import encode_token, token_required
from . import members_bp


@members_bp.route("/login", methods=['POST'])
@limiter.limit("30 per hour")
@cache.cached(timeout=60)
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Member).where(Member.email == email)
    member = db.session.execute(query).scalars().first()

    if member and member.password == password:
        token = encode_token(member.id)

        response = {
                "status" : "success",
                "message": "successfully logged in",
                "token": token
        }

        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password"})


@members_bp.route("/", methods=["POST"])
@limiter.limit("30 per hour")
@cache.cached(timeout=60)
def create_member():
    try:
        member_data = member_schema.load(request.json)
        print(member_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Member).where(Member.email == member_data["email"])
    existing_member = db.session.execute(query).scalars().first()

    if existing_member:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()

    return member_schema.jsonify(new_member), 201


@members_bp.route("/", methods=["GET"])
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()

    return members_schema.jsonify(members)


@members_bp.route("/my-tickets", methods=['GET'])
@token_required
def get_tickets():
    member = db.session.get(Member, member_id)
    customer_id = member['id']

    if customer_id:
        query = select(ServiceTickets).where(service_tickets.id == customer_id)
        tickets = db.session.execute(query).scalars().all()
        return service_tickets_schema.jsonify(tickets)


@members_bp.route("/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = db.session.get(Member, member_id)

    if member:
        return member_schema.jsonify(member), 200
    return jsonify({"error": "Member not found."}), 404


@members_bp.route("/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found"}), 404

    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_email = member_data.get("email")
    if new_email:
        existing_member = (
            db.session.execute(select(Member).where(Member.email == new_email))
            .scalars()
            .first()
        )

    if existing_member and existing_member.id != member_id:
        return jsonify({"error": "Email already with another account."}), 400

    for key, value in member_data.items():
        setattr(member, key, value)

    db.session.commit()
    return member_schema.jsonify(member), 200


@members_bp.route("/<int:member_id>", methods=['DELETE'])
@token_required
def delete_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error" : "Member not found."}), 404

    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f"Member id: {member_id}, successfully deleted."}), 200
