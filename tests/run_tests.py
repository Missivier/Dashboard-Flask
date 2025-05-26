import unittest
import sys
import os

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importer tous les tests
from test_models import TestTaskModel
from test_tasks_routes import TestTasksRoutes
from test_auth_regression import TestAuthRegression

def run_tests():
    """Exécuter tous les tests"""
    # Créer une suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter les tests
    test_suite.addTest(unittest.makeSuite(TestTaskModel))
    test_suite.addTest(unittest.makeSuite(TestTasksRoutes))
    test_suite.addTest(unittest.makeSuite(TestAuthRegression))
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Retourner le code de sortie approprié
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 