import os


class Config:
    """
    General configuration class
    """
    SECRET_KEY ='jhfhlfhw'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://koi:password@localhost/pitch'


class ProdConfig(Config):
    """
    Production configuration class
    """
    pass


class DevConfig(Config):
    """
    Development configuration class
    """
    DEBUG = True


config_options = {
    'production': ProdConfig,
    'development': DevConfig
}
