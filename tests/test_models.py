"""
Test suite for Task model and related functionality.
This module contains unit tests for the Task model, including creation, completion status,
validation, and relationship testing.
"""

import unittest
from app import create_app
from app.models.task import Task, Status, ListTask
from app.models.bdd import init_test_database
from app.models.user import User
from datetime import datetime

class TestTaskModel(unittest.TestCase):
    """
    Test case class for Task model functionality.
    Tests include task creation, completion status, validation, and relationship verification.
    """
    
    def setUp(self):
        """
        Set up test environment before each test case.
        Initializes test database and creates necessary test data including:
        - A test status
        - A test task list
        - A test user
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
        
    def tearDown(self):
        """
        Clean up after each test case.
        Drops all test tables and closes database connection.
        """
        self.db.drop_tables([Task, Status, ListTask, User])
        self.db.close()
        self.app_context.pop()
        
    def test_create_task(self):
        """
        Test task creation functionality.
        Verifies that a task can be created with all required attributes
        and that the relationships are properly established.
        """
        task = Task.create(
            name="Test Task",
            description="Description de test",
            status=self.status,
            list_task=self.list_task,
            user=self.user
        )
        
        self.assertIsNotNone(task.id)
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.description, "Description de test")
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.list_task.name_list_task, "Liste de test")
        self.assertEqual(task.user.name_user, "testuser")
        
    def test_task_completion(self):
        """
        Test task completion status functionality.
        Verifies that task completion status changes correctly when status is updated.
        """
        task = Task.create(
            name="Test Task",
            status=self.status,
            list_task=self.list_task,
            user=self.user
        )
        
        self.assertFalse(task.is_completed)
        
        task.status, _ = Status.get_or_create(name_status="Terminé")
        task.save()
        
        self.assertTrue(task.is_completed)
        
    def test_task_validation(self):
        """
        Test task validation rules.
        Verifies that appropriate errors are raised for invalid task data.
        """
        with self.assertRaises(ValueError):
            Task.create(
                name="",  # Empty name should raise ValueError
                status=self.status,
                list_task=self.list_task,
                user=self.user
            )
            
    def test_task_relationships(self):
        """
        Test task relationships with other models.
        Verifies that task correctly maintains relationships with:
        - Status
        - ListTask
        - User
        """
        task = Task.create(
            name="Test Task",
            status=self.status,
            list_task=self.list_task,
            user=self.user
        )
        
        # Verify relationships
        self.assertEqual(task.status.name_status, "À faire")
        self.assertEqual(task.list_task.name_list_task, "Liste de test")
        self.assertEqual(task.user.name_user, "testuser")

if __name__ == '__main__':
    unittest.main() 