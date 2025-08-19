
from . import service_tickets_bp 
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.blueprints.mechanics.schemas import mechanics_schema
from app.models import Service_Tickets, Mechanics, db
from app.extensions import limiter, cache

#CREATE ROUTE
@service_tickets_bp.route('/service_tickets', methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #Creating service ticket object    
    new_service_ticket = Service_Tickets(**data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_tickets_schema.jsonify(new_service_ticket), 201


#Add mechanic to service ticket
@service_tickets_bp.route('/<int:service_ticket_id>/add-mechanic/<int:mechanic_id>', methods=['PUT'])
@limiter.limit("10 per day", override_defaults=True)
def add_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if mechanic not in service_ticket.mechanics: #checking to see if a relationship already exist between service ticket and mechanic
        service_ticket.mechanics.append(mechanic) #creating a relationship between servicticket and mechanic
        db.session.commit()
        return jsonify({
            'message': f'Successfully Added {mechanic.name} to Service Ticket',
            'service_ticket': service_ticket_schema.dump(service_ticket),  #use dump when the schema is adding just a piece of the return message
            'mechanics': mechanics_schema.dump(service_ticket.mechanics) #using the mechanics_schema to serialize the list of mechanics related to the service ticket
        }), 200
    
    return jsonify("This Mechanic is Already on the Service Ticket"), 400

#Remove book from loan
@service_tickets_bp.route('/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
@limiter.limit("10 per day", override_defaults=True)
def remove_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if mechanic in service_ticket.mechanics: #checking to see if a relationship already exist between service ticket and mechanic
        service_ticket.mechanics.remove(mechanic_id) #removing the relationship between service ticket and mechanic
        db.session.commit()
        return jsonify({
            'message': f'Successfully Removed {mechanic.name} from Service Ticket',
            'service_ticket': service_ticket_schema.dump(service_ticket),  #use dump when the schema is adding just a piece of the return message
            'mechanics': mechanics_schema.dump(loan.books) #using the mechanics_schema to serialize the list of mechanics related to the service ticket
        }), 200
    
    return jsonify("This Mechanic is Not on the Service Ticket"), 400


# #Read S_T
# @service_tickets_bp.route('/service_tickets', methods=["GET"])
# def read_service_tickets():
#     service_tickets = db.session.query(Service_Tickets).all()
#     return service_tickets_schema.jsonify(service_tickets), 200


# #Read Individual S_T - Using a Dynamic Endpoint
# @service_tickets_bp.route('/service_tickets/<int:service_ticket_id>', methods=["GET"])
# def read_service_tickets():
#     service_tickets = db.session.get(Service_Tickets, service_ticket_id)
#     return service_tickets_schema.jsonify(service_tickets), 200


#Delete
@service_tickets_bp.route('/service_tickets/<int:service_ticket_id>', methods=["DELETE"])
def read_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"messgae": f"Successfully Deleted Service_Ticket {service_ticket_id}"}), 200


#Update
@service_tickets_bp.route('/service_tickets/<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id) #Query for our service ticket to update

    if not service_ticket: #Checking if I got a s_t
        return jsonify({"message": "service_ticket not found"}), 404 #if not return error message
    
    try:
        service_ticket_data = service_tickets_schema.load(request.json) #Validating updates
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in service_ticket_data.items():  #Looping over attributes and values from service ticket data dictionary
        setattr(service_ticket, key, value) # setting Object, Attribute, Value to replace

    db.session.commit()
    return service_tickets_schema.jsonify(service_ticket), 200
