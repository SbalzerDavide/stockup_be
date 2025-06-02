from django.db import models
from django.conf import settings

from apps.shopping_list.models import ShoppingList

class Purchase(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, # If the user is deleted, delete purchase
    verbose_name='user'
  )
  
  shopping_list = models.ForeignKey(
    ShoppingList, 
    on_delete= models.SET_NULL,
    null=True,
    blank=True,
    verbose_name='shopping_list'
  )
  
  total_cost = models.FloatField()
  total_items = models.IntegerField(null=True, blank=True)
  
  store = models.TextField(max_length=255, null=True, blank=True)
  
  purchase_date = models.DateTimeField(null=True, blank=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = "purchases"
  
