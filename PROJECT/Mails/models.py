from django.db import models
from tinymce.models import HTMLField


# Create your models here.

greeting_choices=[
    ('Hello','Hello'),
    ('Greetings','Greetings'),
    ('Congratulations','Congratulations'),
    ('Welcome','Welcome')
]

class User_Welcome_Mail(models.Model):
    greeting_type=models.CharField(max_length=400,choices=greeting_choices)
    subject=models.CharField(max_length=4000)
    content=HTMLField()
    class Meta:
        verbose_name_plural = "Welcome Mail - User"

class User_Welcome_Mail_french(models.Model):
    greeting_type=models.CharField(max_length=400,choices=greeting_choices)
    subject=models.CharField(max_length=4000)
    content=HTMLField()