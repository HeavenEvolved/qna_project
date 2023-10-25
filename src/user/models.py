from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT)
    LLM_name = models.CharField(max_length=100)
    LLM_description = models.TextField()

    class Meta:
        app_label = 'genAI'
