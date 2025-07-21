from django.test import TestCase

from apps.hello.models import Message


class MessageModelTest(TestCase):
    def test_greeting_and_response_creation(self) -> None:
        greeting = Message.objects.create(
            content="Test Greeting",
            author_name="Tester",
        )
        response = Message.objects.create(
            content="Test Reply",
            author_name="Tester",
            parent=greeting,
        )
        self.assertEqual(greeting.content, "Test Greeting")
        self.assertEqual(response.content, "Test Reply")
        self.assertEqual(response.author_name, "Tester")
        self.assertEqual(response.parent, greeting)
        # Check relationship
        self.assertIn(response, greeting.responses.all())
