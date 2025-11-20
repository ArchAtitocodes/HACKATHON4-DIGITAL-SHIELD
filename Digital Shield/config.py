import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')
    PORT = os.environ.get('PORT', 5000)
    WORKERS = os.environ.get('WORKERS', 2)
