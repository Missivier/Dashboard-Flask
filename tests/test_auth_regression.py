import unittest
from app import create_app
from app.models.user import User
from app.models.bdd import init_test_database
from werkzeug.security import generate_password_hash

class TestAuthRegression(unittest.TestCase):
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Initialiser la base de données de test
        self.db = init_test_database()
        
        # Créer un utilisateur de test
        self.user = User.create(
            username="testuser",
            email="test@example.com",
            password=generate_password_hash("password123")
        )
        
        # Créer le client de test
        self.client = self.app.test_client()
        
    def tearDown(self):
        """Nettoyage après chaque test"""
        self.db.drop_tables([User])
        self.db.close()
        self.app_context.pop()
        
    def test_login_logout_flow(self):
        """Test du flux de connexion/déconnexion"""
        # Test de connexion
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que l'utilisateur est connecté
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        
        # Test de déconnexion
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que l'utilisateur est déconnecté
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirection vers la page de connexion
        
    def test_login_attempts(self):
        """Test de la protection contre les tentatives de connexion multiples"""
        # Tenter de se connecter avec un mauvais mot de passe
        for _ in range(5):
            response = self.client.post('/auth/login', data={
                'email': 'test@example.com',
                'password': 'wrong_password'
            })
            self.assertEqual(response.status_code, 200)
            
        # Vérifier que le compte est verrouillé
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertIn(b'Compte temporairement verrouill', response.data)
        
    def test_password_reset_flow(self):
        """Test du flux de réinitialisation de mot de passe"""
        # Demander une réinitialisation
        response = self.client.post('/auth/reset-password-request', data={
            'email': 'test@example.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Simuler la réception du token
        token = self.user.get_reset_password_token()
        
        # Réinitialiser le mot de passe
        response = self.client.post(f'/auth/reset-password/{token}', data={
            'password': 'newpassword123',
            'password2': 'newpassword123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que le nouveau mot de passe fonctionne
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'newpassword123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    def test_session_security(self):
        """Test de la sécurité des sessions"""
        # Se connecter
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Vérifier les en-têtes de sécurité
        response = self.client.get('/dashboard')
        self.assertIn('Secure', response.headers.get('Set-Cookie', ''))
        self.assertIn('HttpOnly', response.headers.get('Set-Cookie', ''))
        
    def test_registration_validation(self):
        """Test de la validation lors de l'inscription"""
        # Test avec un email déjà utilisé
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'Email d\xc3\xa9j\xc3\xa0 utilis\xc3\xa9', response.data)
        
        # Test avec un mot de passe trop court
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': '123',
            'password2': '123'
        }, follow_redirects=True)
        self.assertIn(b'Mot de passe trop court', response.data)

if __name__ == '__main__':
    unittest.main() 