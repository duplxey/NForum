from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, default="Another cool user.")
    online = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + "'s profile"
