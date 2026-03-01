from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List
from marshmallow import ValidationError


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


loan_book = db.Table(
        "loan_book",
        Base.metadata,
        db.Column("loan_id", db.ForeignKey("loans.id"), primary_key=True),
        db.Column("book_id", db.ForeignKey("books.id"), primary_key=True),
    )

service_tickets_mechanic_history = db.Table(
        "service_mechanic_history",
        Base.metadata,
        db.Column("service_ticket_id", db.ForeignKey("service_tickets.id"), primary_key=True),
        db.Column("mechanic_id", db.ForeignKey("mechanics.id"), primary_key=True),
    )

service_tickets_customer_history = db.Table(
        "service_customer_history",
        Base.metadata,
        db.Column("service_ticket_id", db.ForeignKey("service_tickets.id"), primary_key=True),
        db.Column("member_id", db.ForeignKey("members.id"), primary_key=True),
    )

service_tickets_inventory = db.Table(
        "service_inventory",
        Base.metadata,
        db.Column("service_ticket_id", db.ForeignKey("service_tickets.id"), primary_key=True),
        db.Column("inventory_id", db.ForeignKey("inventory.id"), primary_key=True),
    )


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    DOB: Mapped[date] = mapped_column(db.Date)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    loans: Mapped[List["Loan"]] = db.relationship(back_populates="member")
    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(
    secondary=service_tickets_customer_history,
    back_populates="members"
)


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(primary_key=True)
    loan_date: Mapped[date] = mapped_column(db.Date)
    member_id: Mapped[int] = mapped_column(db.ForeignKey("members.id"))

    member: Mapped["Member"] = db.relationship(back_populates="loans")
    books: Mapped[List["Book"]] = db.relationship(
        secondary=loan_book, back_populates="loans"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str] = mapped_column(db.String(255), nullable=False)
    genre: Mapped[str] = mapped_column(db.String(255), nullable=False)
    desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    title: Mapped[str] = mapped_column(db.String(255), nullable=False)

    loans: Mapped[List["Loan"]] = db.relationship(
        secondary=loan_book, back_populates="books"
    )


class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(160), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(150), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(db.Float(), nullable=False)

    mechanic_tickets: Mapped[List["MechanicServiceTicket"]] = db.relationship(back_populates="mechanic")
    service_tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_tickets_mechanic_history,
        back_populates="mechanics"
    )


class ServiceTicket(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[int] = mapped_column(db.Float(), nullable=False)
    description: Mapped[str] = mapped_column(db.String(360), nullable=False)
    service_data: Mapped[date]
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"), nullable=False)

    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        secondary=service_tickets_mechanic_history,
        back_populates="service_tickets"
    )

    members: Mapped[List["Member"]] = db.relationship(
        secondary=service_tickets_customer_history,
        back_populates="service_tickets"
    )

    mechanic_tickets: Mapped[List["MechanicServiceTicket"]] = db.relationship(
        "MechanicServiceTicket",
        back_populates="service_ticket"
    )


class MechanicServiceTicket(Base):
    __tablename__ = "MechanicServiceTicket"

    id: Mapped[int] = mapped_column(primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey("mechanics.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(db.ForeignKey("service_tickets.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(db.DateTime, nullable=False)

    mechanic: Mapped["Mechanic"] = db.relationship(back_populates="mechanic_tickets")
    service_ticket: Mapped["ServiceTicket"] = db.relationship(back_populates="mechanic_tickets")


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    price: Mapped[float] = mapped_column(db.Float(), nullable=False)
