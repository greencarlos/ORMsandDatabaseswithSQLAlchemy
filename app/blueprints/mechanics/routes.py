from .schemas import mechanic_schema, mechanics_schema
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from marshmallow import ValidationError
from datetime import date
from app.models import Mechanic, db
from app.extensions import limiter, cache, ma
from . import mechanics_bp


@mechanics_bp.route("/", methods=["POST"])
@limiter.limit("30 per hour")
@cache.cached(timeout=60)
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
        print(mechanic_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Mechanic).where(Mechanic.email == mechanic_data["email"])
    existing_mechanic = db.session.execute(query).scalars().first()

    if existing_mechanic:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics)


@mechanics_bp.route("/<int:mechanic_id>", methods=["GET"])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404


@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_email = mechanic_data.get("email")
    if new_email:
        existing_mechanic = (
            db.session.execute(select(Mechanic).where(Mechanic.email == new_email))
            .scalars()
            .first()
        )

    if existing_mechanic and existing_mechanic.id != mechanic_id:
        return jsonify({"error": "Email already with another account."}), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not mechanic:
        return jsonify({"error" : "Mechanic not found."}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic id: {mechnic_id}, successfully deleted."}), 200
