from app.blueprints.service_tickets import service_tickets_bp 
from .schemas import services_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import VaidationError
from app.models import Service_Tickets, db


#CREATE ROUTE
@service_tickets_bp.route('/service_tickets', methods=['POST'])
def create_service_ticket():
    try:
        data = services_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #Creating S_T object    
    new_service_ticket = Service_Tickets(**data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_tickets_schema.jsonify(new_service_ticket), 201


#Read S_T
@service_tickets_bp.route('/service_tickets', methods=["GET"])
def read_service_tickets():
    service_tickets = db.session.query(Service_Tickets).all()
    return service_tickets_schema.jsonify(service_tickets), 200


#Read Individual S_T - Using a Dynamic Endpoint
@service_tickets_bp.route('/service_tickets/<int:service_ticket_id>', methods=["GET"])
def read_service_tickets():
    service_tickets = db.session.get(Service_Tickets, service_ticket_id)
    return service_tickets_schema.jsonify(service_tickets), 200


#Delete
@service_tickets_bp.route('/service_tickets/<int:service_ticket_id>', methods=["DELETE"])
def read_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"messgae": f"Successfully Deleted Service_Ticket {service_ticket_id}"}), 200


#Update
@service_tickets_bp.route('<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id) #Query for our s_t to update

    if not service_ticket: #Checking if I got a s_t
        return jsonify({"message": "service_ticket not found"}), 404 #if not return error message
    
    try:
        service_ticket_data = service_tickets_schema.load(request.json) #Validating updates
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in service_ticket_data.items():  #Looping over attributes and values from s_t data dictionary
        setattr(service_ticket, key, value) # setting Object, Attribute, Value to replace

    db.session.commit()
    return service_tickets_schema.jsonify(service_ticket), 200
