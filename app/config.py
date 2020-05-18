import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    MONGODB_HOST = os.environ.get('DATABASE_URL') or "mongodb+srv://tsilahadad:Noam3012@michal-sela-dspmm.gcp.mongodb.net/michal-sela?retryWrites=true&w=majority"
       #  "mongodb+srv://Michal_sela:hackathon@cluster0-4bsi2.gcp.mongodb.net/Bad_guys?retryWrites=true&w=majority"


    MONGODB_DB = os.environ.get('DB_NAME') or "Bad_guys"


config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}