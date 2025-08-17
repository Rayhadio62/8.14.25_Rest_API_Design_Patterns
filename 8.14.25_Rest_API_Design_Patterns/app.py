from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, ForeignKey, Float, Table, Column, Integer
from datetime import date
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)
ma = Marshmallow()


db.init_app(app)


service_mechanics = Table(
    "service_mechanics",
    Base.metadata,
    Column("service_tickets_id",Integer, ForeignKey("service_tickets.id")),
    Column("mechanics_id",Integer, ForeignKey("mechanics.id"))
)


class Customers(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(80), nullable=False)
    address: Mapped[str] = mapped_column(String(80), nullable=False)
    
    service_tickets: Mapped[list['Service_Tickets']] = relationship('Service_Tickets', back_populates='customer')
       
    

class Service_Tickets(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    service_desc: Mapped[str] = mapped_column(String(80), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, unique=True)
    vin: Mapped[str] = mapped_column(String(40), nullable=False)
    service_date: Mapped[Date] = mapped_column(Date, nullable=False)
    
  
    customer: Mapped["Customers"] = relationship("Customers", back_populates="service_tickets")
   
    mechanics: Mapped[list["Mechanics"]] = relationship("Mechanics", secondary=service_mechanics, 
                                                        back_populates="service_tickets")
    
                
         
class Mechanics(Base):
    __tablename__ = 'mechanics'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str] = mapped_column(String(80), nullable=False)
    
    service_tickets: Mapped[list["Service_Tickets"]] = relationship("Service_Tickets", secondary=service_mechanics, 
                                                                    back_populates="mechanics")
    

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



with app.app_context():
    db.create_all()
    
app.run(debug=True)
