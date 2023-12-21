
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


    def __str__(self):
        return self.username
    
class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')   

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')