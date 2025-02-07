from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.
class UserManager(auth_models.BaseUserManager):
  def create_user(self, first_name: str, last_name: str, email: str, password: str = None, is_superuser: bool = False, is_staff: bool = False, is_active: bool = True)-> "User":
    if not email:
      raise ValueError("The Email is required")
    if not first_name:
      raise ValueError('The First Name is required')
    if not last_name:
      raise ValueError('The Last Name is required')
    user = self.model(email=self.normalize_email(email))
    user.first_name = first_name
    user.last_name = last_name
    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.is_active = True
    user.set_password(password)
    
    user.save()
    return user
  
  def create_superuser(self, first_name: str, last_name: str, email: str, password: str)-> "User":
    user = self.create_user(
      first_name=first_name, 
      last_name=last_name, 
      email=email, 
      password=password, 
      is_superuser=True, 
      is_staff=True
    )
    user.save()
    return user
class User(auth_models.AbstractUser):
  first_name = models.CharField(verbose_name="First name", max_length=255)
  last_name = models.CharField(verbose_name="Last name", max_length=255)
  email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
  password = models.CharField(verbose_name="Password", max_length=255)
  username = None
  
  objects = UserManager()
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']
  
  class Meta:
    db_table = "users"

  
  
