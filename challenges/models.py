from django.db import models

class ChallengePlatform(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()
    difficulty_level = models.CharField(
        max_length=100, 
        choices=[
            ('Beginner', 'Beginner'), 
            ('Intermediate', 'Intermediate'), 
            ('Advanced', 'Advanced')
        ]
    )
    payment_status = models.CharField(
        max_length=100, 
        choices=[
            ('Paid', 'Paid'),
            ('Unpaid', 'Unpaid'),
            ('Both', 'Both')
        ]
    )
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
