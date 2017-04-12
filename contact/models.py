from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-created_at',)
