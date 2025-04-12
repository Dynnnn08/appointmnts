from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    time = models.TimeField()
    service = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.date} at {self.time}"
