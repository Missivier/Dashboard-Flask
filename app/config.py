"""
Configuration module for the Flask application.
This module defines different configuration classes for various environments
and contains all application settings including security, database, and session configurations.
"""

import os
from datetime import timedelta

class Config:
    """
    Base configuration class containing all default settings.
    This class defines the core configuration parameters used across all environments.
    """
    
    # Base configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', 'csrf_secret_key')
    
    # Database configuration
    DB_NAME = os.environ.get('DB_NAME', 'mydb')
    DB_USER = os.environ.get('DB_USER', 'user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 5432))
    
    # Security configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
    WTF_CSRF_FIELD_NAME = "csrf_token"
    WTF_CSRF_HEADERS = ["X-CSRFToken", "X-CSRF-Token"]
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # CSRF cookie configuration
    CSRF_COOKIE = {
        'samesite': 'Strict',
        'httponly': True,
        'secure': False  # Set to True in production with HTTPS
    }
    CSRF_COOKIE_REFRESH_EACH_REQUEST = True
    
    # Session cookie configuration
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE', 'Strict')
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 3600)))
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB default
    
    # File upload configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Password security configuration
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_PATTERN = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    
    # Rate limiting configuration
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Security headers configuration
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
    }
    
    # Login attempt limiting configuration
    LOGIN_ATTEMPTS_LIMIT = 5
    LOGIN_ATTEMPTS_WINDOW = 300  # 5 minutes in seconds
    LOGIN_ATTEMPTS_BLOCK_DURATION = 900  # 15 minutes in seconds

class DevelopmentConfig(Config):
    """
    Development environment configuration.
    Enables debug mode and other development-specific settings.
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Production environment configuration.
    Disables debug mode and includes additional security settings.
    """
    DEBUG = False
    # Add additional security options here

# For Flask, you can load the config like this:
# app.config.from_object('app.config.DevelopmentConfig')