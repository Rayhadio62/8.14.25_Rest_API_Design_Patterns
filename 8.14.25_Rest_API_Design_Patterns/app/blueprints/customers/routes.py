
from . import customers_bp 
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db
from app.extensions import limiter, cache


#CREATE ROUTE
@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #Creating object    
    new_customer = Customers(**data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


#Read
@customers_bp.route('/customers', methods=["GET"])
def read_customers():
    customers = db.session.query(Customers).all()
    return customers_schema.jsonify(customers), 200


#Read Individual Mechanic - Using a Dynamic Endpoint
@customers_bp.route('/customers/<int:customer_id>', methods=["GET"])
def read_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    return customers_schema.jsonify(customer), 200


#Delete
@customers_bp.route('/customer/<int:customer_id>', methods=["DELETE"])
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"messgae": f"Successfully Deleted Customer {customer_id}"}), 200


#Update
@customers_bp.route('<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id) #Query for our mechanic to update

    if not customer: #Checking if I got a mechanic
        return jsonify({"message": "Customer Not Found"}), 404 #if not return error message
    
    try:
        customer_data = customer_schema.load(request.json) #Validating updates
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in customer_data.items(): #Looping over attributes and values from mechanic data dictionary
        setattr(customer, key, value) # setting Object, Attribute, Value to replace

    db.session.commit()
    return customer_schema.jsonify(customer), 200