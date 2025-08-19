
class DevelopementConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    Cache_Type = "SimpeCache"
    Cache_Defualt_timeout = 300
    
    
class TestingConfig:
    pass

class ProductionConfig:
    pass