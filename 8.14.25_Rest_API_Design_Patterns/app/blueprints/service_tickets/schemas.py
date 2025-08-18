from app.extensions import ma
from app.models import Service_Tickets


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tickets
        include_FK = True
        

service_ticket_schema = Service_TicketSchema() 
service_tickets_schema = Service_TicketSchema(many=True)