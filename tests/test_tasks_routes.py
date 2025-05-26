"""
Test suite for Task-related routes and API endpoints.
This module contains integration tests for task-related routes, including:
- Task listing
- Task creation
- Task modification
- Task deletion
- Task filtering
"""

import unittest
from app import create_app
from app.models.task import Task, Status, ListTask
from app.models.bdd import init_test_database
from app.models.user import User
from flask_login import login_user

class TestTasksRoutes(unittest.TestCase):
    """
    Test case class for Task-related routes.
    Tests include CRUD operations and filtering functionality for tasks.
    """
    
    def setUp(self):
        """
        Set up test environment before each test case.
        Initializes test database, creates test data, and sets up test client
        with an authenticated user session.
        """
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Initialize test database
        self.db = init_test_database()
        
        # Create test data
        self.status, _ = Status.get_or_create(name_status="À faire")
        self.list_task, _ = ListTask.get_or_create(name_list_task="Liste de test")
        self.user = User.create(
            name_user="testuser",
            username_user="testuser1",
            first_name_user="Test",
            last_name_user="User",
            email_user="test@example.com",
            password="password123"
        )
        
        # Create test client
        self.client = self.app.test_client()
        
        # Log in user for authenticated requests
        with self.client.session_transaction() as session:
            login_user(self.user)
        
    def tearDown(self):
        """
        Clean up after each test case.
        Drops all test tables and closes database connection.
        """
        self.db.drop_tables([Task, Status, ListTask, User])
        self.db.close()
        self.app_context.pop()
        
    def test_index_route(self):
        """
        Test the main tasks listing route.
        Verifies that the tasks page loads successfully and contains expected content.
        """
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tasks', response.data)
        
    def test_create_task(self):
        """
        Test task creation through the API.
        Verifies that a new task can be created via POST request
        and that the task is properly saved with all attributes.
        """
        response = self.client.post('/tasks/create', data={
            'name': 'Nouvelle tâche',
            'description': 'Description de test',
            'status': self.status.id,
            'list_task': self.list_task.id
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        task = Task.get_or_none(Task.name == 'Nouvelle tâche')
        self.assertIsNotNone(task)
        self.assertEqual(task.description, 'Description de test')
        self.assertEqual(task.list_task.name_list_task, "Liste de test")
        self.assertEqual(task.user.name_user, "testuser")
        
    def test_edit_task(self):
        """
        Test task modification through the API.
        Verifies that an existing task can be updated via POST request
        and that the changes are properly saved.
        """
        task = Task.create(
            name="Tâche à modifier",
            status=self.status,
            list_task=self.list_task,
            user=self.user
        )
        
        response = self.client.post(f'/tasks/{task.id}/edit', data={
            'name': 'Tâche modifiée',
            'description': 'Nouvelle description',
            'status': self.status.id,
            'list_task': self.list_task.id
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        task.refresh()
        self.assertEqual(task.name, 'Tâche modifiée')
        self.assertEqual(task.description, 'Nouvelle description')
        
    def test_delete_task(self):
        """
        Test task deletion through the API.
        Verifies that a task can be deleted via POST request
        and that it is properly removed from the database.
        """
        task = Task.create(
            name="Tâche à supprimer",
            status=self.status,
            list_task=self.list_task,
            user=self.user
        )
        
        response = self.client.post(f'/tasks/{task.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Task.get_or_none(Task.id == task.id))
        
    def test_filter_tasks(self):
        """
        Test task filtering functionality.
        Verifies that tasks can be filtered by status
        and that the correct tasks are displayed in the response.
        """
        # Create tasks with different statuses
        completed_status, _ = Status.get_or_create(name_status="Terminé")
        Task.create(
            name="Tâche 1",
            status=self.status,
            list_task=self.list_task,
            user=self.user
        )
        Task.create(
            name="Tâche 2",
            status=completed_status,
            list_task=self.list_task,
            user=self.user
        )
        
        # Test status filter
        response = self.client.get('/tasks/?status=Terminé')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tâche 2'.encode('utf-8'), response.data)
        self.assertNotIn('Tâche 1'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main() 