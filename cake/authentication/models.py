from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Rolechoice(models.TextChoices):

    ADMIN = 'Admin','Admin'

    USER = 'User','User'

    


class Profile(AbstractUser):

    role = models.CharField(max_length=20,choices=Rolechoice.choices)


    class Meta :

        verbose_name = 'Profile'

        verbose_name_plural = 'Profiles'


    def __str__(self):

        return self.username
    



