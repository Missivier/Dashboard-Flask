from flask import Flask, g, jsonify
from flask_login import LoginManager
from app.models.bdd import db, init_database
from app.models.user import User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'votre_clé_secrète_ici'  # À changer en production
    
    # Initialiser Flask-Login
    login_manager.init_app(app)
    
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
    from app.routes.auth import auth
    from app.routes.main import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

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
