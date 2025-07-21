from django.db import models


# Shared abstract base for author
class AuthorMixin(models.Model):
    author_name = models.CharField(max_length=100, default="Anonymous")

    class Meta:
        abstract = True


class Greeting(AuthorMixin):
    message = models.CharField(max_length=200, default="Hello, World!")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message


class Response(AuthorMixin):
    greeting = models.ForeignKey(
        Greeting, on_delete=models.CASCADE, related_name="responses"
    )
    reply = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.author_name}: {self.reply}"
