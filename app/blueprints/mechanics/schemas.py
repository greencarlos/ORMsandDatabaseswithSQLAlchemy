from app.extensions import ma
from app.models import Mechanic 

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_relationships = False


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
