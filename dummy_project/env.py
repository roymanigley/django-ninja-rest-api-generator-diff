import os


class MissingEnvironmentVariableException(BaseException):
    pass


# RUNTIME ENVIRONMENT VARIABLES
APP_TOKEN_EXPIRATION_MINUTES = os.getenv('TOKEN_EXPIRATION_MINUTES', 60 * 24 * 365)
APP_SECRET_KEY = os.getenv("APP_SECRET", "local-secret-JLKDSAJIOWE67DSA9878965DSADAD1234098DSASA")
APP_ENV = os.getenv("APP_ENV", "LOCAL")
APP_DEBUG = APP_ENV != 'PROD' and os.getenv("APP_DEBUG", "FALSE").upper() == "TRUE"
APP_DATABASE_URL = os.getenv('DATABASE_URL')

if APP_DATABASE_URL is None:
    raise MissingEnvironmentVariableException('environment variable "DATABASE_URL" is missing')
