from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
        ('DONE', 'Done'),
    ]

    APPOINTMENT_TYPES = [
        ('GENERAL', 'General Checkup'),
        ('DENTAL', 'Dental'),
        ('CARDIOLOGY', 'Cardiology'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES, default='GENERAL')
    date = models.DateField()
    time = models.TimeField()
    symptoms_of_illness = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True)

    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')
        
    def __str__(self):
        return f"{self.user.username} - {self.get_appointment_type_display()} on {self.date} at {self.time} - {self.status}"

    class Meta:
        ordering = ['-date', '-time']