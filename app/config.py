import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    DB_NAME = os.environ.get('DB_NAME', 'mydb')
    DB_USER = os.environ.get('DB_USER', 'user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', 'csrf_secret_key')
    # Ajoute ici d'autres configs (mail, API, etc.)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Ajoute ici des options de sécurité supplémentaires

# Pour Flask, tu peux charger la config ainsi :
# app.config.from_object('app.config.DevelopmentConfig')