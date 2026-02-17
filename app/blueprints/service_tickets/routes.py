from .schemas import service_ticket_schema, service_tickets_schema, mechanic_schema
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from marshmallow import ValidationError
from datetime import date
from app.models import ServiceTicket, Members, db
from app.extensions import limiter, cache, ma
from . import service_tickets_bp


@service_tickets_bp.route("/", methods=["POST"])
@limiter.limit("30 per hour")
@cache.cached(timeout=60)
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
        print(service_ticket_data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_data["id"])
    existing_service_ticket = db.session.execute(query).scalars().first()

    if existing_service_ticket:
        return jsonify({"error": "id already associated with an account."}), 400

    new_service_ticket = ServiceTicket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201


@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    query = select(ServiceTicket)
    service_tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(service_tickets)


@service_tickets_bp.route("/<int:service_ticket_id>", methods=["GET"])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if service_ticket:
        return service_ticket_schema.jsonify(service_ticket), 200
    return jsonify({"error": "Service Ticket not found."}), 404


@service_tickets_bp.route("/<int:service_ticket_id>/edit", methods=['PUT'])
def remove_mechanic(remove_ids, add_ids):

    try:
        mechanic_data = mechanic_schema.load(request.json)
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(ServiceTicket)
        service_ticket = db.paginate(query, page=page, per_page=per_page)
    except:
        query = select(ServiceTicket)
        service_ticket = db.session.execute(query).scalars().all()
        return service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp.route("/<int:service_ticket_id>", methods=["PUT"])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service Ticket not found"}), 404

    try:
        service_ticket_data = service_ticket_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    service_ticket_data.pop("id", None)
    new_id = service_ticket_data.get("id")

    if new_id:
        existing_service_ticket = (
            db.session.execute(select(ServiceTicket).where(ServiceTicket.id == new_id))
            .scalars()
            .first()
        )

    for key, value in service_ticket_data.items():
        setattr(service_ticket, key, value)

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp.route("/<int:service_ticket_id>", methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if not service_ticket:
        return jsonify({"error" : "Service Ticket not found."}), 404

    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service ticket id: {service_ticket_id}, successfully deleted."}), 200
