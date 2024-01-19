from os import environ as env

IMAGES_FOLDER = env.get('IMAGES_FOLDER') or 'app/static/images'
IMAGES_DEFAULT_NAME = 'default.jpg'


class Config:
    TESTING = False
    DEVELOPMENT = False
    DEBUG = False
    APP_SECRET_KEY = env.get('APP_SECRET') or b"secret"
    IMAGES_FOLDER = IMAGES_FOLDER
    IMAGES_DEFAULT_NAME = IMAGES_DEFAULT_NAME

    JWT_TOKEN_SECRET = "Bearer"

    def get_secret_key(self):
        return self.APP_SECRET_KEY

    @staticmethod
    def get_profile(profile_name: str = None):
        config = {
            DevProfile.ENV_NAME: DevProfile(),
            TestProfile.ENV_NAME: TestProfile(),
            ProdProfile.ENV_NAME: ProdProfile()
        }
        default_config = DevProfile.ENV_NAME
        return config.get(env.get('APP_CONFIG') or profile_name or default_config)


class DevProfile(Config):
    DEVELOPMENT = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL') or 'sqlite:///laboratory_work.db'
    ENV_NAME = 'development'


class TestProfile(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL') or 'sqlite:///laboratory_test.db'
    ENV_NAME = 'test'
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:5000'


class ProdProfile(Config):
    SQLALCHEMY_DATABASE_URI = (env.get('DATABASE_URL')
                               or 'postgresql://postgres:postgres@localhost:5432/postgres')
    ENV_NAME = 'prod'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
