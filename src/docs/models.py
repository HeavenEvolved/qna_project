from django.db import models

# Create your models here.
class File(models.Model):
    upload = models.FileField(upload_to='files/')
    
    def __str__(self):
        return str(self.pk)