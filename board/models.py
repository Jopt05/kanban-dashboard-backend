from django.db import models

from profiles.models import UserProfile

# Create your models here.

class Board(models.Model):
    title = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )

    def get_title(self):
        return self.title
    
    def __str__(self):
        return self.title