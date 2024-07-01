from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User
# from .views import validate_password_strength

# Create your models here.


class Book(models.Model):
    BOOK_CATEGORY = [
        ('romance', 'Romance'),
        ('horror', 'Horror'),
        ('fantasy', 'Fantasy'),
        ('science_fiction', 'Science Fiction'),
        ('history', 'History')
    ]
    bId = models.IntegerField(null=False, unique=True)
    bName = models.CharField(max_length=255, null=False)
    bAuthor = models.CharField(max_length=100, null=False)
    bCategory = models.CharField( max_length=100, choices=BOOK_CATEGORY, null=False)
    bDescription = models.TextField(max_length=1000)
    bPublishDate = models.DateField(validators=[MaxValueValidator(timezone.now().date())]) 
    bCoverImage = models.ImageField(upload_to='book_covers/',null=False, blank=True, default="images/13.jpg")

class SignUp(models.Model):
    ACCOUNT_TYPE = [
        ('Admin', 'Admin'),
        ('User', 'User')
    ]
    FirstName = models.CharField(max_length=25, default="")
    LastName = models.CharField(max_length=25, default="")
    usernamee = models.CharField(max_length=50, unique=True, default="")
    Email = models.EmailField(max_length=100, unique=True, default="")
    Password = models.CharField(max_length=50, validators=[MinLengthValidator(8)], default="")
    AccType = models.CharField( max_length=100, choices=ACCOUNT_TYPE)    
    
    # def __str__(self):
    #     return f'{self.user.username} - SignUp'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    

class AdminAcc(models.Model):
    FirstName = models.CharField(max_length=25)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    
class UserAcc(models.Model):
    FirstName = models.CharField(max_length=25)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    
    
    
# class LogIn(models.Model):
#     Username = models.CharField(max_length=50, unique=True, default="")
#     Password = models.CharField(max_length=50, validators=[MinLengthValidator(8)], default="")