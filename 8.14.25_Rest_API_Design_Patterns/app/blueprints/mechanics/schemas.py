from app.extensions import ma
from app.models import Mechanics


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        include_FK = True
        

mechanic_schema = MechanicSchema() 
mechanics_schema = MechanicSchema(many=True)
