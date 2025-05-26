"""
Security middleware module for the Flask application.
This module provides security-related functionality including:
- Security headers management
- Login attempt tracking and rate limiting
- Session-based security controls
"""

from flask import request, current_app, session
from functools import wraps
import time
from datetime import datetime, timedelta

def apply_security_headers(response):
    """
    Applies security headers to all HTTP responses.
    
    Args:
        response: The Flask response object to modify
        
    Returns:
        Response: The modified response with security headers
    """
    for header, value in current_app.config['SECURITY_HEADERS'].items():
        response.headers[header] = value
    return response

def track_login_attempts():
    """
    Manages and tracks login attempts for rate limiting.
    
    This function:
    1. Cleans up old login attempts
    2. Checks if the user is currently blocked
    3. Resets blocking if the block period has expired
    
    Returns:
        bool: True if login is allowed, False if blocked
    """
    if 'login_attempts' not in session:
        session['login_attempts'] = []
    
    # Clean up old attempts
    current_time = time.time()
    session['login_attempts'] = [
        attempt for attempt in session['login_attempts']
        if current_time - attempt < current_app.config['LOGIN_ATTEMPTS_WINDOW']
    ]
    
    # Check if user is blocked
    if len(session['login_attempts']) >= current_app.config['LOGIN_ATTEMPTS_LIMIT']:
        block_until = session.get('block_until', 0)
        if current_time < block_until:
            return False
        
        # Reset blocking if period has passed
        session.pop('block_until', None)
        session['login_attempts'] = []
    
    return True

def record_login_attempt():
    """
    Records a new login attempt and manages blocking.
    
    This function:
    1. Records the timestamp of the attempt
    2. Implements blocking if too many attempts are made
    3. Manages the blocking duration
    """
    if 'login_attempts' not in session:
        session['login_attempts'] = []
    
    session['login_attempts'].append(time.time())
    
    # Block if too many attempts
    if len(session['login_attempts']) >= current_app.config['LOGIN_ATTEMPTS_LIMIT']:
        session['block_until'] = time.time() + current_app.config['LOGIN_ATTEMPTS_BLOCK_DURATION']

def login_attempts_required(f):
    """
    Decorator to protect login routes with rate limiting.
    
    This decorator:
    1. Checks if the user is allowed to attempt login
    2. Returns a 429 status code if blocked
    3. Allows the login attempt if not blocked
    
    Args:
        f: The route function to protect
        
    Returns:
        function: The decorated function with rate limiting
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not track_login_attempts():
            return "Trop de tentatives de connexion. Veuillez réessayer plus tard.", 429
        return f(*args, **kwargs)
    return decorated_function 