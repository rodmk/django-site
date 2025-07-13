from django.test import TestCase
from .models import Greeting, Response


class GreetingResponseModelTest(TestCase):
    def test_greeting_and_response_creation(self) -> None:
        greeting = Greeting.objects.create(message="Test Greeting")
        response = Response.objects.create(
            greeting=greeting, reply="Test Reply", sender_name="Tester"
        )
        self.assertEqual(greeting.message, "Test Greeting")
        self.assertEqual(response.reply, "Test Reply")
        self.assertEqual(response.sender_name, "Tester")
        self.assertEqual(response.greeting, greeting)
        # Check relationship
        self.assertIn(response, greeting.responses.all())
