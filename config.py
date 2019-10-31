class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'cxYFqST8YcuK6wZV6Aoy-P_JBVYXBMSUlLBV2WsCKWQ'
 
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://lynko:lynko@localhost/academy'

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
 
    URL_VERSION = "/api/v1"

    JWT_ACCESS_LIFESPAN = {'hours': 24}
    JWT_REFRESH_LIFESPAN = {'days': 30}
    JWT_HEADER_TYPE = "halley"
    # DISABLE_PRAETORIAN_ERROR_HANDLER = 1