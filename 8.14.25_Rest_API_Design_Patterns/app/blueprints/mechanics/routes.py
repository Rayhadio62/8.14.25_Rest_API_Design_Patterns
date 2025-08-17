from app.blueprints.mechanics import mechanics_bp 
from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import VaidationError
from app.models import Mechanics, db


#CREATE ROUTE
@app.route('/mechanics', methods=['POST'])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #Creating object    
    new_mechanic = Mechanics(**data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


#Read
@app.route('/mechanics', methods=["GET"])
def read_mechanics():
    mechanics = db.session.query(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200


#Read Individual Mechanic - Using a Dynamic Endpoint
@app.route('/mechanics/<int:mechanic_id>', methods=["GET"])
def read_mechanics():
    mechanics = db.session.get(Mechanics, mechanic_id)
    return mechanics_schema.jsonify(mechanic), 200


#Delete
@app.route('/mechanic/<int:mechanic_id>', methods=["DELETE"])
def read_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechnaic_id)
    db.session,delete(mechanic)
    db.session.commit()
    return jsonify({"messgae": f"Successfully Deleted Mechanic {mechanic_id}"}), 200


#Update
@mechanics_bp.route('<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    user = db.session.get(Mechanics, mechanic_id) #Query for our mechanic to update

    if not mechanic: #Checking if I got a mechanic
        return jsonify({"message": "mechanic not found"}), 404 #if not return error message
    
    try:
        mechanic_data = mechanic_schema.load(request.json) #Validating updates
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in mechanic_data.items(): #Looping over attributes and values from mechanic data dictionary
        setattr(user, key, value) # setting Object, Attribute, Value to replace

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

