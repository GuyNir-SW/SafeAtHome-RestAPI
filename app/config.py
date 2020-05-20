import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    MONGODB_HOST = os.environ.get('DATABASE_URL')


    MONGODB_DB = os.environ.get('DB_NAME') or "Bad_guys"


config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}
