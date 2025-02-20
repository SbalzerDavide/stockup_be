from django.db import models
from django.conf import settings

class ShoppingList(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, # If the user is deleted, delete shopping list
    verbose_name='user'
  )
  
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  
  is_active = models.BooleanField()
  is_purchased = models.BooleanField()
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "shopping_lists"

  def __str__(self):
    return self.name