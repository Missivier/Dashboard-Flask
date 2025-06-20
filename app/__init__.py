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

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # Initialiser Flask-Login
    login_manager.init_app(app)
    
    # Initialiser la protection CSRF
    csrf.init_app(app)
    
    # Configuration des en-têtes CSRF
    app.config['WTF_CSRF_HEADERS'] = ['X-CSRFToken', 'X-CSRF-Token']
    app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']
    
    # Gestionnaire d'erreurs CSRF
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify({
            'error': 'Erreur de validation CSRF',
            'message': 'Le token CSRF est manquant ou invalide. Veuillez rafraîchir la page et réessayer.'
        }), 400
    
    # Middleware pour rafraîchir le token CSRF
    @app.after_request
    def refresh_csrf_token(response):
        if 'csrf_token' not in g:
            g.csrf_token = generate_csrf()
        return response
    
    # Initialiser la base de données
    init_database()
    
    # Sécurité : Limiter les requêtes (anti-bruteforce)
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "20 per minute"]
    )
    
    # Sécurité : Headers HTTP avec CSP adaptée pour CDN
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
    
    # Enregistrer les blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(tasks)
    app.register_blueprint(pets_bp)
    app.register_blueprint(budgets)
    app.register_blueprint(calendar_bp)

    # Ouvrir une connexion à chaque requête
    @app.before_request
    def before_request():
        if db.is_closed():
            db.connect()
        g.db = db

    # Fermer la connexion après la requête
    @app.teardown_request
    def teardown_request(exception):
        if not db.is_closed():
            db.close()

    @app.route('/')
    def index():
        return jsonify({
            "status": "success",
            "message": "L'application Flask est en cours d'exécution !"
        })

    return app
