class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:BAC146@localhost/library_db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite://testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    pass
