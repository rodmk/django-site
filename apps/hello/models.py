from django.db import models


class Message(models.Model):
    author_name = models.CharField(max_length=100, default="Anonymous")
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="responses",
    )

    def __str__(self) -> str:
        return f"{self.author_name}: {self.content}"
