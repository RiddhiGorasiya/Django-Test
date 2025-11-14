from django.db import models
from django.contrib.auth.models import User as AuthUser

class User(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Project Manager', 'Project Manager'),
        ('Developer', 'Developer'),
    ]

    user = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Developer')
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users')
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"


# from django.db import models
# from django.contrib.auth.models import User 
# # from django.contrib.auth.models import AbstractUser

# # Create your models here.
# class User(models.Model):

#     ROLE_CHOICES = [
#         ('Admin', 'Admin'),
#         ('Project Manager', 'Project Manager'),
#         ('Developer', 'Developer'),
#     ]
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)
#     name = models.CharField(max_length=100, blank=True) # blank=True dose not show error_messages
#     email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=100)
#     role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Developer')

#     def __str__(self):
#         return f"{self.name} ({self.role})"    

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     role = models.CharField(max_length=50)
#     created_by = models.ForeignKey(User, related_name='created_profiles', on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return self.user.username

# # class User(AbstractUser):
# #     role = models.CharField(max_length=50, choices=[('Developer', 'Developer'), ('Project Manager', 'Project Manager')])
