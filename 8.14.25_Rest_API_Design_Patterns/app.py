
from app.models import db
from app import create_app
# from app.blueprints.mechanics import mechanics_bp


app = create_app('DevelopmentConfig')


with app.app_context():
     db.create_all()
    
app.run()


