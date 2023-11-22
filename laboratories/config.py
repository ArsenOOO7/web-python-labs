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

    def get_secret_key(self):
        return self.APP_SECRET_KEY

    @staticmethod
    def get_profile():
        config = {
            DevProfile.ENV_NAME: DevProfile(),
            TestProfile.ENV_NAME: TestProfile(),
            ProdProfile.ENV_NAME: ProdProfile()
        }
        default_config = 'development'
        return config.get(env.get('APP_CONFIG') or default_config)


class DevProfile(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env.get('DEV_DATABASE_URI') or 'sqlite:///laboratory_work.db'
    ENV_NAME = 'development'


class TestProfile(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = env.get('TEST_DATABASE_URI') or 'sqlite:///test.db'
    ENV_NAME = 'test'


class ProdProfile(Config):
    SQLALCHEMY_DATABASE_URI = env.get('PROD_DATABASE_URI') or 'sqlite:///web_course.db'  # Maybe Postgres is better
    ENV_NAME = 'prod'
