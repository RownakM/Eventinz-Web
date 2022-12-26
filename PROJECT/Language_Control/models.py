from django.db import models

# Create your models here.

CHOICES = {
    ('Enable','Enable'),
    ('Disable','Disable')
}

class Language_Control(models.Model):
    english_text = models.TextField()
    french_text = models.TextField()
    status = models.CharField(max_length = 40,choices = CHOICES,default ='Disable')
    class Meta:
        verbose_name_plural = "Language Control"