from django.db import models

# Create your models here.
class ItemMacronutriments(models.Model):
  name = models.CharField(max_length=255)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "item_macronutriments"

  def __str__(self):
    return self.name