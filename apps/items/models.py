from django.db import models
from django.conf import settings

from apps.item_categories.models import ItemCategories

class Items(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, # If the user is deleted, delete the preferences
    verbose_name='user'
  )
  
  category = models.ForeignKey(
    ItemCategories, 
    on_delete= models.SET_NULL,
    null=True,
    blank=True,
    verbose_name='category'
  )

  name = models.CharField(max_length=255)
  consumation_average_days = models.FloatField(null=True, blank=True)
  department = models.TextField(max_length=255, null=True, blank=True)
  is_edible = models.BooleanField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "items"

  def __str__(self):
    return self.name
