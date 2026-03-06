from app.extensions import ma
from app.models import Mechanic 
from marshmallow import fields

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_relationships = False

    name = fields.String(required=True)
    email = fields.Email(required=True)
    phone = fields.String(required=True)
    salary = fields.Float(required=False)


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
