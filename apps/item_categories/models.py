from django.db import models
from django.conf import settings

class ItemCategories(models.Model):
  user = models.ForeignKey(
  settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, # If the user is deleted, delete the preferences
    verbose_name='user'
  )

  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "item_categories"

  def __str__(self):
    return self.name
