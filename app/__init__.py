"""
Flask application factory and initialization module.
This module sets up the Flask application with all necessary extensions,
security configurations, and database connections.
"""

from flask import Flask, g, jsonify
from flask_login import LoginManager
from app.models.bdd import db, init_database
from app.models.user import User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect, CSRFError, generate_csrf
from app.config import DevelopmentConfig
from app.routes.main import main
from app.routes.auth import auth
from app.routes.tasks import tasks
from app.routes.pet_routes import bp as pets_bp
from app.routes.budgets import budgets
from app.routes.calendar import calendar_bp
from app.middleware import apply_security_headers
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize Flask-Login for user authentication
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    """
    User loader callback for Flask-Login.
    Retrieves a user from the database by their ID.
    
    Args:
        user_id: The ID of the user to load
        
    Returns:
        User: The user object if found, None otherwise
    """
    return User.get_by_id(user_id)

def create_app():
    """
    Application factory function that creates and configures the Flask application.
    
    This function:
    1. Creates the Flask application
    2. Configures security settings
    3. Initializes extensions
    4. Registers blueprints
    5. Sets up database connection handling
    
    Returns:
        Flask: The configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # Initialize Flask-Login for user authentication
    login_manager.init_app(app)
    
    # Initialize database connection
    init_database()
    
    # Security: Rate limiting to prevent brute force attacks
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "20 per minute"]
    )
    
    # Security: HTTP headers with CSP configured for CDN usage
    csp = {
        'default-src': [
            "'self'",
            'https://cdn.tailwindcss.com',
            'https://cdn.jsdelivr.net'
        ],
        'script-src': [
            "'self'",
            'https://cdn.tailwindcss.com'
        ],
        'style-src': [
            "'self'",
            'https://cdn.jsdelivr.net',
            "'unsafe-inline'"
        ]
    }
    Talisman(app, content_security_policy=csp)
    
    # Apply custom security headers
    app.after_request(apply_security_headers)
    
    # Register application blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(tasks)
    app.register_blueprint(pets_bp)
    app.register_blueprint(budgets)
    app.register_blueprint(calendar_bp)

    @app.before_request
    def before_request():
        """
        Ensure database connection is open before each request.
        Stores the database connection in Flask's g object for request context.
        """
        if db.is_closed():
            db.connect()
        g.db = db

    @app.teardown_request
    def teardown_request(exception):
        """
        Close database connection after each request.
        
        Args:
            exception: Any exception that occurred during the request
        """
        if not db.is_closed():
            db.close()

    @app.route('/')
    def index():
        """
        Root endpoint that returns a simple JSON response
        indicating the application is running.
        
        Returns:
            JSON: A success message indicating the application is running
        """
        return jsonify({
            "status": "success",
            "message": "L'application Flask est en cours d'exécution !"
        })

    return app
