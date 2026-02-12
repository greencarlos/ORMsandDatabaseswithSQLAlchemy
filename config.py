class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:pa$$w0rd!@localhost/library_db"
    DEBUG = True


class TestingConfig:
    pass

class ProductionConfig:
    pass

