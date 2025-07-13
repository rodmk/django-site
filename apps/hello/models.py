from django.db import models


class Greeting(models.Model):
    message = models.CharField(max_length=200, default="Hello, World!")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Response(models.Model):
    greeting = models.ForeignKey(
        Greeting, on_delete=models.CASCADE, related_name="responses"
    )
    reply = models.CharField(max_length=200)
    sender_name = models.CharField(max_length=100, default="Anonymous")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_name}: {self.reply}"
