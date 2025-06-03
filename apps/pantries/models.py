from django.conf import settings
from django.db import models

class Pantry(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, # If the user is deleted, delete pantry
    verbose_name='user'
  )
  
  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "pantries"

