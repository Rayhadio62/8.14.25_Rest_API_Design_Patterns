class DevelopmentConfig:
    SQLALCHEMY.DATABASE.URI = 'sqlite:///app.db'
    DEBUG = True
    
class TestingConfig:
    pass

class ProductionConfig:
    pass