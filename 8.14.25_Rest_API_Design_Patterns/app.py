
from app.models import db
from app import create_app

app = create_app('DevelopementConfig')

with app.app_context():
    db.create_all()
    
app.run()


