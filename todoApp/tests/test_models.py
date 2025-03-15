from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import ToDone

class ToDoneModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a test todo
        self.todo = ToDone.objects.create(
            title='Test Todo',
            description='This is a test todo description',
            user=self.user
        )

    def test_todo_creation(self):
        """Test if todo is created with correct attributes"""
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.description, 'This is a test todo description')
        self.assertEqual(self.todo.user, self.user)
        self.assertIsNotNone(self.todo.sn)
        self.assertIsNotNone(self.todo.date)

    def test_todo_string_representation(self):
        """Test the string representation of the todo"""
        expected_string = f'{self.todo.title} ---- {self.todo.date}'
        self.assertEqual(str(self.todo), expected_string)

    def test_todo_user_relationship(self):
        """Test the relationship between todo and user"""
        self.assertEqual(self.todo.user.username, 'testuser')
        # Test cascade delete
        self.user.delete()
        self.assertEqual(ToDone.objects.count(), 0)

    def test_todo_auto_fields(self):
        """Test if auto fields are properly set"""
        # Test if sn is auto-incrementing
        todo2 = ToDone.objects.create(
            title='Second Todo',
            description='Another test todo',
            user=self.user
        )
        self.assertGreater(todo2.sn, self.todo.sn)

        # Test if date is automatically set
        self.assertIsNotNone(self.todo.date)
        self.assertLessEqual(self.todo.date, timezone.now()) 