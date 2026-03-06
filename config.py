import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pa$$w0rd!@localhost/library_db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.version.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = 'SimpleCache'
    pass
