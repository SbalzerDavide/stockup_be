from django.db import models
from django.conf import settings

class UserPreferences(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, # If the user is deleted, delete the preferences
    verbose_name='user'
  )
  
  class PreferenceType(models.TextChoices):
        PREFERENCE = 'preference', 'Preference'
        INTOLLERANCE = 'intolerance', 'Intolerance'
        ALLERGIES = 'allergies', 'Allergies'
            
  preference_type = models.CharField(
    max_length=20,
    choices=PreferenceType.choices,
    default=PreferenceType.INTOLLERANCE
  )
  
  value = models.CharField(max_length=255) # es. “Vegetariano”, “Senza glutine”
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    db_table = "user_preferences"
  
  def __str__(self):
    return self.user.email