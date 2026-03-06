from .schemas import inventory_schema, inventories_schema 
from app.blueprints.service_tickets.schemas import service_tickets_schema  
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from marshmallow import ValidationError
from datetime import date
from app.models import Inventory, db
from app.extensions import limiter, cache, ma
from app.utils.util import encode_token, token_required
from . import inventory_bp


@inventory_bp.route("/", methods=["POST"])
@limiter.limit("30 per hour")
@cache.cached(timeout=60)
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
        print(inventory_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Inventory).where(Inventory.name == inventory_data["name"])
    existing_inventory = db.session.execute(query).scalars().first()

    if existing_inventory:
        return jsonify({"error": "Inventory name already exists."}), 400

    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()

    return inventory_schema.jsonify(new_inventory), 201


@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    query = select(Inventory)
    inventory = db.session.execute(query).scalars().all()

    return inventories_schema.jsonify(inventory)


@inventory_bp.route("/<int:inventory_id>", methods=["GET"])
def get_inventory_id(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if inventory:
        return inventory_schema.jsonify(inventory), 200
    return jsonify({"error": "Inventory not found."}), 404


@inventory_bp.route("/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error": "Inventory not found"}), 404

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_inventory = inventory_data.get("name")
    if new_inventory:
        existing_inventory = (
            db.session.execute(select(Inventory).where(Inventory.name == new_inventory))
            .scalars()
            .first()
        )

    if existing_inventory and existing_inventory.id != inventory_id:
        return jsonify({"error": "Inventory already exists."}), 400

    for key, value in inventory_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
def delete_inventory(inventory_id):
    print(f"inventory id: {inventory_id}")
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error" : "Inventory not found."}), 404

    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f"Inventory id: {inventory_id}, successfully deleted."}), 200
