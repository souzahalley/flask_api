class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'cxYFqST8YcuK6wZV6Aoy-P_JBVYXBMSUlLBV2WsCKWQ'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://lynko:lynko@localhost/academy'
    URL_VERSION = "/api/v1"