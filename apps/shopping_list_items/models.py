from django.db import models
from django.conf import settings

from apps.items.models import Items
from apps.shopping_list.models import ShoppingList

class ShoppingListItems(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, # If the user is deleted, delete shopping list item
    verbose_name='user'
  )
  
  item = models.ForeignKey(
    Items,
    on_delete=models.CASCADE, # If the item is deleted, delete shopping list item
    verbose_name='user'
  )
  
  shopping_list = models.ForeignKey(
    ShoppingList,
    on_delete=models.CASCADE, # If the shopping list is deleted, delete shopping list item
    verbose_name='shopping list',
  )
  
  is_checked = models.BooleanField()
  is_proposed = models.BooleanField()
  
  quantity = models.IntegerField()
  
  weight = models.FloatField(blank=True, null=True)
  unit_weight = models.CharField(max_length=255, blank=True, null=True)
  
  volume = models.FloatField(blank=True, null=True)
  unit_volume = models.CharField(max_length=255, blank=True, null=True)
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "shopping_list_items"

  def __str__(self):
    return self.name