import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS= True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    
    # Setup default language
    BABEL_DEFAULT_LOCALE = "en"
    # Your application default translation path
    BABEL_DEFAULT_FOLDER = "translations"
    # The allowed translation for you app
    LANGUAGES = {
        "es": {"flag": "es", "name": "Spanish"},
        "en": {"flag": "gb", "name": "English"},
        "pt": {"flag": "pt", "name": "Portuguese"},
        "pt_BR": {"flag": "br", "name": "Pt Brazil"},
        "de": {"flag": "de", "name": "German"},
        "zh": {"flag": "cn", "name": "Chinese"},
        "ru": {"flag": "ru", "name": "Russian"},
        "pl": {"flag": "pl", "name": "Polish"},
    }