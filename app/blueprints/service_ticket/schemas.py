from app.extensions import ma
from app.models import Member

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket 
        include_relationships = False


service_ticket_schema = ServiceTicketSchema()
service_ticket_schema = ServiceTicketSchema(many=True)
