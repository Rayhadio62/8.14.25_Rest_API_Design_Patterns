from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, ForeignKey, Float, Table, Column, Integer
from datetime import date
from flask_marshmallow import Marshmallow


















    

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        
user_schema = UserSchema()
users_schema = UsersSchema(many=True)
        
#CREATE USER ROUTE
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #Creating user object    
    new_user = Users(**data)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201


#Read Users
@app.route('/users', methods=["GET"])
def read_users():
    users = db.session.query(Users).all()
    return users_schema.jsonify(users), 200


#Read Individual User - Using a Dynamic Endpoint
@app.route('/users/<int:user_id>', methods=["GET"])
def read_users():
    users = db.session.get(Users, user_id)
    return users_schema.jsonify(user), 200


#Delete a user
@app.route('/users/<int:user_id>', methods=["DELETE"])
def read_user(user_id):
    user = db.session.get(Users, user_id)
    db.session,delete(user)
    db.session.commit()
    return jsonify({"messgae": f"Successfully Deleted User {user_id}"}), 200


#Update a User
@users_bp.route('<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(Users, user_id) #Query for our user to update

    if not user: #Checking if I got a user
        return jsonify({"message": "user not found"}), 404  #if not return error message
    
    try:
        user_data = user_schema.load(request.json) #Validating updates
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    for key, value in user_data.items(): #Looping over attributes and values from user data dictionary
        setattr(user, key, value) # setting Object, Attribute, Value to replace

    db.session.commit()
    return user_schema.jsonify(user), 200
    
#Query the user by id
#Validate and Deserialze the updates that they are sending in the body of the request
#for each of the values that they are sending, we will change the value of the queried object
#commit the changes
#return a response


with app.app_context():
    db.create_all()
    
app.run(debug=True)
