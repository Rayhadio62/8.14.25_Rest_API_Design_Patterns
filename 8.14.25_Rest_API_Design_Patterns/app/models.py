
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, String, ForeignKey, Float, String, Table, Column, Integer
from datetime import datetime, timedelta



class Base(DeclarativeBase):
    pass





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

